### conda install diagrams
from diagrams import Cluster, Diagram, Edge
from diagrams.custom import Custom
import os
os.environ['PATH'] += os.pathsep + 'C:/Program Files/Graphviz/bin/'

graphattr = {     #https://www.graphviz.org/doc/info/attrs.html
    'fontsize': '22',
}

nodeattr = {   
    'fontsize': '22',
    'bgcolor': 'lightyellow'
}

eventedgeattr = {
    'color': 'red',
    'style': 'dotted'
}
evattr = {
    'color': 'darkgreen',
    'style': 'dotted'
}
with Diagram('cargosystemArch', show=False, outformat='png', graph_attr=graphattr) as diag:
  with Cluster('env'):
     sys = Custom('','./qakicons/system.png')
### see https://renenyffenegger.ch/notes/tools/Graphviz/attributes/label/HTML-like/index
     with Cluster('ctxcargo', graph_attr=nodeattr):
          hold=Custom('hold','./qakicons/symActorWithobjSmall.png')
          cargoservice=Custom('cargoservice','./qakicons/symActorWithobjSmall.png')
          cargorobot=Custom('cargorobot','./qakicons/symActorWithobjSmall.png')
          led=Custom('led','./qakicons/symActorWithobjSmall.png')
          markerdevice=Custom('markerdevice','./qakicons/symActorWithobjSmall.png')
          sonar=Custom('sonar','./qakicons/symActorWithobjSmall.png')
     with Cluster('ctxrobotsmart', graph_attr=nodeattr):
          robotsmart=Custom('robotsmart(ext)','./qakicons/externalQActor.png')
     cargorobot >> Edge(color='magenta', style='solid', decorate='true', label='<find_slot_position<font color="darkgreen"> slot_position</font> &nbsp; >',  fontcolor='magenta') >> hold
     cargoservice >> Edge(color='magenta', style='solid', decorate='true', label='<do_marking<font color="darkgreen"> marking_done</font> &nbsp; >',  fontcolor='magenta') >> markerdevice
     cargoservice >> Edge(color='magenta', style='solid', decorate='true', label='<find_free_slot<font color="darkgreen"> slot_found slot_full</font> &nbsp; find_release<font color="darkgreen"> release_done</font> &nbsp; find_occupy<font color="darkgreen"> occupy_done</font> &nbsp; >',  fontcolor='magenta') >> hold
     cargorobot >> Edge(color='magenta', style='solid', decorate='true', label='<moverobot<font color="darkgreen"> moverobotdone moverobotfailed</font> &nbsp; >',  fontcolor='magenta') >> robotsmart
     cargoservice >> Edge(color='magenta', style='solid', decorate='true', label='<robot_to_ioport<font color="darkgreen"> robot_ioport_done robot_ioport_failed</font> &nbsp; robot_to_slot5<font color="darkgreen"> robot_slot5_done robot_slot5_failed</font> &nbsp; robot_to_slot<font color="darkgreen"> robot_slot_done robot_slot_failed</font> &nbsp; >',  fontcolor='magenta') >> cargorobot
     sonar >> Edge(color='blue', style='solid',  decorate='true', label='<container_detected &nbsp; sonar_fault &nbsp; sonar_recovered &nbsp; >',  fontcolor='blue') >> cargoservice
     hold >> Edge(color='blue', style='solid',  decorate='true', label='<slot_is_free &nbsp; slot_is_full &nbsp; >',  fontcolor='blue') >> hold
     cargoservice >> Edge(color='blue', style='solid',  decorate='true', label='<led_blink &nbsp; >',  fontcolor='blue') >> led
diag
