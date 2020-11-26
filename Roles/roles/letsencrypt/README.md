Install Let's Encrypt to Create SSL Certificates
==================================

https://www.linode.com/docs/security/ssl/install-lets-encrypt-to-create-ssl-certificates/


#===> Before you BeginPermalink
Update your server’s software packages:

CentOS
    sudo yum update && sudo yum upgrade

Debian / Ubuntu
    sudo apt update && sudo apt upgrade


#===> Download and Install Let’s EncryptPermalink
Install the git package:

CentOS
    sudo yum install git

Debian / Ubuntu
    sudo apt-get install git

Download a clone of Let’s Encrypt from the official GitHub repository. /opt is a common installation directory for third-party packages, so let’s install the clone to /opt/letsencrypt:

    sudo git clone https://github.com/letsencrypt/letsencrypt /opt/letsencrypt

Navigate to the new /opt/letsencrypt directory:
    cd /opt/letsencrypt


#===> Create an SSL CertificatePermalink
Let’s Encrypt automatically performs Domain Validation (DV) using a series of challenges. The Certificate Authority (CA) uses challenges to verify the authenticity of your computer’s domain. Once your Linode has been validated, the CA will issue SSL certificates to you.

Run Let’s Encrypt with the --standalone parameter. For each additional domain name requiring a certificate, add -d example.com to the end of the command.

    sudo -H ./letsencrypt-auto certonly --standalone -d example.com -d www.example.com


#===> Check Certificate DomainsPermalink
The output of the Let’s Encrypt script shows where your certificate is stored; in this case, /etc/letsencrypt/live:

    sudo ls /etc/letsencrypt/live

All of the domains you specified above will be covered under this single certificate. This can be verified as follows:
    ./certbot-auto certificates


#===> MaintenancePermalink
#===> Renew SSL CertificatesPermalink
Return to the /opt/letsencrypt directory:
    cd /opt/letsencrypt

Execute the command you used in Step 1 of the Create an SSL Certificate section, adding the --renew-by-default parameter:
    sudo -H ./letsencrypt-auto certonly --standalone --renew-by-default -d example.com -d www.example.com


#===> Automatically Renew SSL Certificates (Optional)Permalink
You can also automate certificate renewal. This will prevent your certificates from expiring, and can be accomplished with cron.

The output of the previous command shows how to non-interactively renew all of your certificates:
    ./letsencrypt-auto renew

Set this task to run automatically once per month using a cron job:
    sudo crontab -e

Add the following line to the end of the crontab file:
crontab
    0 0 1 * * /opt/letsencrypt/letsencrypt-auto renew


#===> Update Let’s EncryptPermalink
Return to the /opt/letsencrypt directory:
    cd /opt/letsencrypt

Download any changes made to Let’s Encrypt since you last cloned or pulled the repository, effectively updating it:
    sudo git pull


#===> Automatically Update Let’s Encrypt (Optional)Permalink
You can also use cron to keep the letsencrypt-auto client up to date.
    sudo crontab -e
crontab
    0 0 1 * * cd /opt/letsencrypt && git pull