  echo -e "\e[31mNote: Please ensure that config files in /etc/pam.d/ are restored to as they were before WSL-Hello-sudo was installed\e[m"
  set -x
  sudo rm -rf /etc/pam_wsl_hello
  sudo rm "/lib/x86_64-linux-gnu/security/pam_wsl_hello.so"
  rm -rf /mnt/c/Users/Pierre-Yves/pam_wsl_hello
