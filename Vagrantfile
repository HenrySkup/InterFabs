
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "base"
  config.vm.box_url = "https://cloud-images.ubuntu.com/vagrant/trusty/current/trusty-server-cloudimg-amd64-vagrant-disk1.box"
  config.vm.network :forwarded_port, guest: 612, host: 612
  config.vm.provision :puppet do |puppet|
     puppet.manifests_path = "provision/manifests"
     puppet.manifest_file  = "default.pp"
     puppet.module_path = "provision/modules"
     puppet.options = ['--verbose']
  end
end
