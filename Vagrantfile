# -*- mode: ruby -*-
# vi: set ft=ruby :
# AUTHOR: Luis Alberto López Álvarez - TFM (ETSIT - UPM)

Vagrant.configure("2") do |config|
  # Creación del plugin necesario para poder realizar reinicios
  class RebootPlugin < Vagrant.plugin('2')
    name 'Reboot Plugin'
    # Este plugin proporciona un provisionador llamado my_custom_reboot.
    provisioner 'my_custom_reboot' do
      # Crea el provisionador.
      class RebootProvisioner < Vagrant.plugin('2', :provisioner)
        # Inicialización, define el estado interno. No se necesita nada.
        def initialize(machine, config)
          super(machine, config)
        end
        # Configuración a realizar. Tampoco se necesita nada aquí.
        def configure(root_config)
          super(root_config)
        end
        # Ejecuta el aprovisionamiento.
        def provision
          command = 'shutdown -r now'
          @machine.ui.info("Emitiendo comando: #{command}")
          @machine.communicate.sudo(command) do |type, data|
            if type == :stderr
              @machine.ui.error(data)
            end
          end
          begin
            sleep 5
          end until @machine.communicate.ready?
        end
      end
      RebootProvisioner
    end
  end
  config.vm.box = "kalilinux/rolling"
  # Configuración de la máquina
  config.ssh.insert_key = false
  config.vm.hostname = "DarkWeb-OSINT"
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "6144"
    vb.cpus = "6"
    vb.gui = true
    vb.customize ["modifyvm", :id,"--name", "DarkWeb-OSINT"]
  end
  config.vm.network "forwarded_port", guest: 22, host: 2220, id: "ssh"
  # Evitar la sincronización de carpetas compartidas
  config.vm.synced_folder ".", "/vagrant", disabled: true
  # Inyección del proyecto en la máquina virtual
  config.vm.provision "file", source: "/Users/luis/Desktop/TFM/Aprovisionamiento/tor-scraper-classifier/", destination: "/home/vagrant/Desktop/"
  # Ejecución de los scripts de aprovisionamiento
  config.vm.provision "shell", path: "Aprovisionamiento/tor-scraper-classifier/scripts/setup.sh"
  # Uso del provisionador de reinicio definido en el plugin inicial
  config.vm.provision "my_custom_reboot"
  config.vm.provision "shell", path: "Aprovisionamiento/tor-scraper-classifier/scripts/start.sh"
end


