cat ~/.ssh/id_rsa.pub | ssh root@<domain> "sudo sshcommand acl-add dokku <description>"
#Description can be anything (e.g. your user name or location