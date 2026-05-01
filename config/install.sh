echo "Welcome to the installer for pyWG GUI!"
echo "Retrieving latest version..."
git clone https://github.com/nympp/py-vpnmanager.git
echo "Please look at py-vpnmanager/config/settings.conf and change your settings"
echo "Installation will begin..."
printf "Continue? [y/N]"
read answer

if [ "$answer" = "Y" ] || [ "$answer" = "y" ]; then
    # Moving the program to the desired path
    . ./py-vpnmanager/config/settings.conf
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