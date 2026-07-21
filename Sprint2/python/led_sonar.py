import machine, time, network
from umqtt.simple import MQTTClient

# =========================================================================
# CONFIGURAZIONE RETE E BROKER MQTT
# =========================================================================
SSID = "sas"
PASSWORD = "glglglgl"
BROKER_IP = "10.158.187.242"
BROKER_PORT = 1883

# Topic MQTT specifico dell'attore 'sonar' per l'invio dei Dispatch
# e topic per il controllo del LED
SONAR_TOPIC = b"unibo/qak/sonar"
LED_TOPIC = b"cargo/led/cmd"

# =========================================================================
# CONFIGURAZIONE HARDWARE (PINS)
# =========================================================================
# LED integrato
led = machine.Pin("LED", machine.Pin.OUT)
led.value(0)

# Sensore ad ultrasuoni HC-SR04
TRIG = machine.Pin(0, machine.Pin.OUT)
ECHO = machine.Pin(2, machine.Pin.IN)
TRIG.value(0)

# =========================================================================
# FUNZIONI DI UTILITÀ
# =========================================================================
def connect_wifi():
    """Connette la scheda alla rete Wi-Fi specificata."""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    print("Connessione Wi-Fi in corso...")
    while not wlan.isconnected():
        time.sleep(0.5)
    print("Wi-Fi Connesso! IP:", wlan.ifconfig()[0])

def read_distance_cm():
    """
    Legge la distanza dal sensore HC-SR04 in centimetri.
    In caso di timeout o fuori portata, restituisce 120.0 cm (> DFREE=100cm)
    in modo che il sistema QAk possa eventualmente gestire lo stato di sonar_fault.
    """
    TRIG.value(0)
    time.sleep_us(2)
    TRIG.value(1)
    time.sleep_us(10)
    TRIG.value(0)
    
    try:
        # Timeout a 25ms (~430 cm max)
        duration = machine.time_pulse_us(ECHO, 1, 25000)
    except OSError:
        return 120.0
        
    if duration < 0:
        return 120.0  # Fuori portata o nessun ostacolo
        
    return duration / 58.0

# =========================================================================
# GESTIONE MESSAGGI IN INGRESSO (LED)
# =========================================================================
blinking = False

def on_msg(topic, msg):
    """Callback richiamata alla ricezione di messaggi sul topic LED."""
    global blinking
    print(f"Messaggio ricevuto su {topic.decode()}: {msg.decode()}")
    if msg == b"on":
        blinking = True
        print("LED -> Lampeggio ATTIVATO")
    elif msg == b"off":
        blinking = False
        led.value(0)
        print("LED -> SPENTO")

# =========================================================================
# AVVIO E CICLO PRINCIPALE
# =========================================================================
connect_wifi()

client = MQTTClient("pico_sonar_led", BROKER_IP, BROKER_PORT)
client.set_callback(on_msg)
client.connect()
client.subscribe(LED_TOPIC)

print(f"Sottoscritto al topic LED: {LED_TOPIC.decode()}")
print(f"Invio messaggi Sonar al topic dell'attore sonar: {SONAR_TOPIC.decode()}")

BLINK_INTERVAL_MS = 500
SONAR_PUBLISH_INTERVAL_MS = 300  # ~10 letture in 3 secondi per debounce QAk

led_phys_state = False
last_toggle = time.ticks_ms()
last_sonar_publish = time.ticks_ms()
msg_seq_num = 1

while True:
    # Controlla la presenza di nuovi messaggi MQTT
    client.check_msg()
    now = time.ticks_ms()
    
    # --- Gestione Lampeggio LED ---
    if blinking:
        if time.ticks_diff(now, last_toggle) >= BLINK_INTERVAL_MS:
            led_phys_state = not led_phys_state
            led.value(led_phys_state)
            last_toggle = now
            
    # --- Gestione Lettura e Invio Dati Sonar ---
    if time.ticks_diff(now, last_sonar_publish) >= SONAR_PUBLISH_INTERVAL_MS:
        dist = read_distance_cm()
        
        # Busta ApplMessage di tipo DISPATCH diretta specificamente all'attore 'sonar'
        # Formato: msg(MSGID, dispatch, SENDER, RECEIVER, CONTENT, SEQNUM)
        qak_msg = f"msg(sensor_data, dispatch, pico_sonar, sonar, sensorData({dist:.1f}), {msg_seq_num})"
        
        client.publish(SONAR_TOPIC, qak_msg)
        print(f"Sonar [{dist:.1f} cm] -> Inviato: {qak_msg}")
        
        msg_seq_num += 1
        last_sonar_publish = now
        
    time.sleep_ms(20)