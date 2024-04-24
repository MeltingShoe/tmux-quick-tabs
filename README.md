# tmux-quick-tabs
Allows you to add multiple "tabs" inside a pane that you can quickly switch between. There are many ways to switch between multiple views, and this same functionality can be achieved in different(easier) ways. Right now this is just a small personal project and it's very unpolished. If anyone does use this let me know what you think.


Now we have tpm support! So if you wanna use this just add
```
set -g @plugin 'meltingshoe/NED-QT'
```

Right now the bind to delete tabs does not work and it does a poor job of managing state so I wouldn't recommend installing this unless you're comfortable with managing session manually. If you end up with a lot of "dead" tabs that are stuck in the buffer without being tied to a pane you can type prefix C-x to destroy all of the panes in the buffer, leaving you with just the windows/panes in your active session.


Right now I'm working on refactoring this plugin. It's gonna be cool and have an integrated sessionizer  :)
