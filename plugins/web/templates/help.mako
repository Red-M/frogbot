<!DOCTYPE html>
<html lang="en">
  <head>
    <link rel="shortcut icon" href="http://www.aperturescience.com/favicon.ico" />
	<%include file="__header_data.mako"/>
  </head>
  <body>
    <%include file="__navhelp.mako"/>
    <div class="container">
      <div class="hero-unit">
        <h1>${nick}</h1>
        <p></p>
        <p><a href="http://bit.ly/QHNNMl" class="btn btn-primary btn-large">Hey. &raquo;</a></p>
      </div>
      <div class="row">
          <h2>Help</h2>
           <p>This FrogBot should display extra information on a command when ",help <command>" is used. Also using ",help" by itself will display all the commands the bot has.</p>
           <p>If the command you asked for does not work or you recieve the reply "Nope.avi" then you either are not high enough in this bot's permissions to use this command or you did something wrong...</p>
           <p>Some commands may not have any help information from ",help <command>" because the command may not have any yet...</p>
      </div>
      <hr>
      <footer>
        <%include file="__footer.mako"/>
      </footer>
    </div>
  </body>
</html>
