webersprinkler v2.0

Design Diagram

+-------------+     +-------------+     +-----------------+     +-------------+
| Android App |     | Text Client |     | Other Interface |     | Web Browser |
+------+------+     +------+------+     +--------+--------+     +------+------+
       |                   |                     |                     |
       |                   |                     |                     |
       +-------------------+---------------------+                     |
                           |                                           | HTML/JavaScript from /webfiles
                           | JSON from /API                            | JSON from /API via AJAX
                           |                                           |
                           |           +-------------------+           |   
                           +_----------| Apache Web Server |-----------+
                                       +---+-----------+---+
                                           |           |
                                +----------+---+   +---+------------+
                                |     /API     |   |    /webfiles   |  
                                |  Python App  |   |    Files for   |
                                | via mod_wsgi |   | Browser Access |
                                +--------------+   +----------------+
