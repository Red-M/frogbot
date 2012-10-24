<!DOCTYPE html>
<html lang="en">
  <head>
    <link rel="shortcut icon" href="http://www.aperturescience.com/favicon.ico" />
	<%include file="__header_data.mako"/>
  </head>
  <body>
    <%include file="__nav.mako"/>
    <div class="container">
      <div class="hero-unit">
        <h1>${nick}</h1>
        <p><a href="http://bit.ly/QHNNMl" class="btn btn-primary btn-large">Hey. &raquo;</a></p>
      </div>
      <div class="row">
        <div class="span4">
          <h2>channels</h2>
          <p>The channels and IRC networks this FrogBot is in are:</p>
          % for chan in channels:
            % for chanss in chan:
              ${chanss}
            % endfor
          % endfor
          <p><a class="btn btn-danger" href="/status">View details &raquo;</a></p>
        </div>
        <div class="span4">
          <h2>factoids</h2>
           <p>This FrogBot has factoids that can be used by saying in an unmuted channel "?<factoid name>".</p> 
           <p>The button below will display this Frogbot's complete list of every factoid it has.</p>
          <p><a class="btn btn-danger" href="/factoids">View details &raquo;</a></p>
       </div>
        <div class="span4">
          <h2>other</h2>
          <p>This Frogbot is running from:</p>
          <p>	- <a href="http://${host}">${host}</a></p>
          <p>	- <a href="http://www.python.org/">${pyver}</a></p>
          <p>	- ${os} ${bit}</p>
          <p></p>
          <p>${uptime}</p>
          <p>${mem}</p>
          <p>Players that have tried to join my fake Minecraft Classic server: ${players}</p>
          <p><a class="btn btn-danger" href="/status">View details &raquo;</a></p>
        </div>
      </div>
      <hr>
      <footer>
        <%include file="__footer.mako"/>
      </footer>
    </div>
  </body>
</html>
