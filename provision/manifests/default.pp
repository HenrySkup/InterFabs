

Exec { path => [ "/bin/", "/sbin/" , "/usr/bin/", "/usr/sbin/" ] }

exec { 'apt-get update':
  command => 'apt-get update',
  timeout => 60,
  tries   => 3
}

package { ['python-software-properties']:
  ensure  => 'installed',
  require => Exec['apt-get update'],
}

$sysPackages = [ 'build-essential', 'git', 'curl']
package { $sysPackages:
  ensure => "installed",
  require => Exec['apt-get update'],
}

exec { "/usr/sbin/locale-gen --no-archive en_US.UTF-8":
  creates => '/usr/lib/locale/en_US.utf8',
}

class { 'nodejs':
  version => 'stable',
  target_dir => '/bin',
}