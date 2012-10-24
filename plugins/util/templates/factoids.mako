<!DOCTYPE html>
<html lang="en">
  <head>
    <link rel="shortcut icon" href="http://www.aperturescience.com/favicon.ico" />
	<%include file="__header_data.mako"/>
  </head>
  <body>
    <%include file="__navfacts.mako"/>
    <div class="container">
      <div class="hero-unit">
        <h1>${nick}</h1>
        <p></p>
        <p><a href="http://bit.ly/QHNNMl" class="btn btn-primary btn-large">Hey. &raquo;</a></p>
      </div>
      <h2>Factoids</h2>
<table table border="1" style="table-layout: fixed; width: 100%">
% for cmdss in word:
<li>${cmdss}</li>
<table table border="1" style="table-layout: fixed; width: 100%">
  <tr>
    <th>word</th>
    <th>data</th>
    <th>nick of creator</th>
  </tr>
% for wordata in word[cmdss]:
  <tr>
    ${wordata}
  </tr>
% endfor
</table>
<p></p>
% endfor
</table>
      <hr>
      <footer>
        <%include file="__footer.mako"/>
      </footer>
    </div>
  </body>
</html>
