<!DOCTYPE html>
<html lang="en">
  <head>
    <link rel="shortcut icon" href="http://www.aperturescience.com/favicon.ico" />
	<%include file="__header_data.mako"/>
  </head>
  <body>
    <%include file="__navcommands.mako"/>
    <div class="container">
      <div class="hero-unit">
        <h1>${nick}</h1>
        <p></p>
        <p><a href="http://bit.ly/QHNNMl" class="btn btn-primary btn-large">Hey. &raquo;</a></p>
      </div>
      <div class="row">
      <div class="span${cmdlen}">
      <h2>Commands</h2>
      % for cmdss in commands:
        <div class="span">
          % for cmd in cmdss:
            <li>${cmd}</li>
          % endfor
        </div>
      % endfor
      </div>
      </div>
      <hr>
      <footer>
        <%include file="__footer.mako"/>
      </footer>
    </div>
  </body>
</html>
