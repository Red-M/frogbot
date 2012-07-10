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
        <h1>&#x0ca0;&#x2323;&#x0cb0;&#x0cc3; ${nick} &#x0ca0;&#x2323;&#x0cb0;&#x0cc3;</h1>
        <p></p>
        <p><a href="http://heyyeyaaeyaaaeyaeyaa.com/" class="btn btn-primary btn-large">&#x0ca0;&#x2323;&#x0ca0; Potato &#x0ca0;&#x2323;&#x0ca0; &raquo;</a></p>
      </div>
      <div class="row">
        <div class="span4">
          <h2>channels</h2>
          % for chan in channels:
            % for chanss in chan:
              ${chanss}
            % endfor
          % endfor
          <p><a class="btn btn-danger" href="/status">View details &raquo;</a></p>
        </div>
        <div class="span4">
          <h2>factoids</h2>
           <p>EXAMPLE TEXT.</p>
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
          <p><a class="btn btn-danger" href="#">View details &raquo;</a></p>
        </div>
      </div>
      <hr>
      <footer>
        <%include file="__footer.mako"/>
      </footer>
    </div>
  </body>
</html>
