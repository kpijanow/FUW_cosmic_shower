Projekt dotyczy obserwacji strumienia promieniowania kosmicznego wykorzystując system detektorów programu QuarkNet, który obejmuje sieć instytucji monitorujących promieniowanie kosmiczne. Szczegółowy opis projektu znajduje się w pliku raport.pdf.


Intstukcja instalacji programu do monitorowania promieniowania kosmicznego na Raspberry Pi:

Po zainstalowaniu systemu (zalecany: Rasbian GNU/Linux 8.0) należy otworzyć terminal (CTRL + ALT + T) i wpisać kolejno:

  cd Desktop
  git clone https://github.com/kpijanow/FUW_cosmic_shower.git
  git checkout visuals
  cd FUW_cosmic_shower
  cp launcher.sh ../
  cd ..
  chmod +x launcher.sh

Następnie do pliku /home/pi/.config/lxsession/LXDE-pi/autostart należy dodać linię:
@/home/pi/Desktop/launcher.sh

W przypadku awarii programu należy zrestartować system, program uruchomi się automatycznie.
