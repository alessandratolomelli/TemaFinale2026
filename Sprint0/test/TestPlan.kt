// testplan.kt
//
// Test plan:

class CargoServiceTest {

    // CS-01: richiesta con hold libera -> accepted, stato ENGAGED
    fun testLoadRequestAccepted() {
        val cargoservice = CargoService()
        cargoservice.goto(State.DISENGAGED)

        val reply = cargoservice.handle(LoadRequest())

        assertTrue(reply is LoadAccepted)
        assertEquals("slot1", (reply as LoadAccepted).slotId)
        assertEquals(State.ENGAGED, cargoservice.currentState())
    }

    // CS-02: richiesta con hold piena -> refused, stato resta DISENGAGED
    // NB: non implementabile allo stato attuale: cargoservice non è collegato
    // alla Hold, quindi non esiste una condizione reale di "hold piena".
    // Test lasciato come TODO/placeholder per quando la Hold sarà integrata.
    fun testLoadRequestRefused_WhenHoldFull() {
        val cargoservice = CargoService()
        // TODO: iniettare una Hold con slot1-4 tutti occupati, quando disponibile
        // val hold = Hold(slot1 = true, slot2 = true, slot3 = true, slot4 = true)
        // cargoservice.attachHold(hold)

        val reply = cargoservice.handle(LoadRequest())

        assertTrue(reply is LoadRefused)
        assertEquals(State.DISENGAGED, cargoservice.currentState())
    }

    // CS-03: richiesta con IOPort occupato / sistema fuori servizio -> retrylater
    // NB: stesso discorso di CS-02, manca ancora la condizione reale che triggeri
    // questo esito (nessun collegamento a sonar/stato "out of service").
    fun testLoadRequestRetryLater_WhenIOPortBusy() {
        val cargoservice = CargoService()
        // TODO: simulare IOPort occupato o sistema "out of service"

        val reply = cargoservice.handle(LoadRequest())

        assertTrue(reply is LoadRetryLater)
        assertEquals(State.DISENGAGED, cargoservice.currentState())
    }

}

class IOPortTest {

    // IO-01: pressione pulsante -> invio loadRequest
    fun testPushButton_SendsLoadRequest() {
        val ioport = IOPort()
        ioport.goto(State.PRESS_BUTTON)

        val sentRequest = ioport.pressButton()

        assertTrue(sentRequest is LoadRequest)
    }

    // IO-02: ricezione loadAccepted -> stato "accepted", mostra slot assegnato
    fun testReceiveLoadAccepted_UpdatesDisplay() {
        val ioport = IOPort()

        ioport.onReply(LoadAccepted(slotId = "slot1"))

        assertEquals(State.ACCEPTED, ioport.currentState())
        assertEquals("slot1", ioport.displayedSlot())
    }

    // IO-03: ricezione loadRetryLater -> stato "retrylater"
    fun testReceiveLoadRetryLater_UpdatesDisplay() {
        val ioport = IOPort()

        ioport.onReply(LoadRetryLater())

        assertEquals(State.RETRYLATER, ioport.currentState())
    }

    // IO-04: ricezione loadRefused -> stato "refused"
    fun testReceiveLoadRefused_UpdatesDisplay() {
        val ioport = IOPort()

        ioport.onReply(LoadRefused())

        assertEquals(State.REFUSED, ioport.currentState())
    }

}