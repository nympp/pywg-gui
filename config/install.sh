# Buggy, do not use for now
# Installation method :
# $ git clone https://github.com/nympp/py-vpnmanager
# $ cd py-vpnmanager/
# $ config/install.sh

echo "Welcome to the installer for pyWG GUI!"
echo "Please look at 'config/settings.conf' and change your settings"
echo "REMINDER! pyWG GUI requires 'wireguard-tools' package installed!"
echo "Installation will begin..."
printf "Continue? [y/N]"
read answer

if [ "$answer" = "Y" ] || [ "$answer" = "y" ]; then
    # Moving the program to the desired path
    . ./settings.conf # reads settings.conf
    mkdir "$INSTALLPATH"
    mv py-vpnmanager/* "$INSTALLPATH"
    # Adding "pywg" as a command
    cd "$INSTALLPATH"
    sudo chmod +x config/pywg
    sudo mv pywg /bin
else
    echo "User stopped the installation. Begin cleaning"
    rm -rf py-vpnmanager
    echo "Cleaned. Exiting."
fi