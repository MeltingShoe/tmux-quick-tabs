# tmux-quick-tabs
Allows you to add multiple "tabs" inside a pane that you can quickly switch between. There are many ways to switch between multiple views, and this same functionality can be achieved in different(easier) ways. Right now this is just a small personal project and it's very unpolished. If anyone does use this let me know what you think.


Now we have tpm support! So if you wanna use this just add
```
set -g @plugin 'meltingshoe/tmux-quick-tabs'
```

Right now the bind to delete tabs does not work and it does a poor job of managing state so I wouldn't recommend installing this unless you're comfortable with managing session manually. If you end up with a lot of "dead" tabs that are stuck in the buffer without being tied to a pane you can type prefix C-x to destroy all of the panes in the buffer, leaving you with just the windows/panes in your active session.

Right now I'm working on refactoring this plugin. It's gonna be cool and have an integrated sessionizer  :)

TODO: 
define a set of tabs to always be shared(ie .tmux.conf init.lua) that you can switch into any tab
  they're like, temporary. So you can always press a button to start swapping into those tabs and when you press the normal swap button it goes back
Same thing but for extra project files
  so when you're working on 2-3 files in a repo it could go and open all the other files in that repo in the extra tab
  works largely the same as global shared tabs
  but there's a button to add the current tab into the tab group
  and when you close tabs they can be send here instead
Slide-over tab group
  ipad slide over
  just a floating window
  probably have to attach it to a session tho which will be hard
tabs are fixed

