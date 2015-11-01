* Add the Dockerfile to the root of your static files
* Init the git repository and/or add the remote of your dokku app

    git remote add dokku git@yourdomain.com:appname

* Commit all your changes and the repository

   git commit -am Pushing to dokku
   git push dokku master

* Optionally, add any extra domains with the domains plugin:

   ssh dokku@yourdomain.com domains:add appname domain.com


Find all the available commands and help:

   ssh dokku@yourdomain.com
   
   