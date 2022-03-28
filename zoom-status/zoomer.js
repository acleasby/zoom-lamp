#!/usr/bin/osascript -l JavaScript


var app = Application.currentApplication();
app.includeStandardAdditions = true;

var desktopString = app.pathTo("desktop").toString()
var STATE_FILE = `${desktopString}/zoom-state.txt`

function run(argv) {

  var isZoom = false, isMeeting = false, audioStatus = "muted", videoStatus = "muted";

  if(Application("zoom.us").running()) {
    isZoom = true;
    var se = Application("System Events");
    var zoom = se.processes.byName("zoom.us");

    var meeting = zoom.menuBars[0].menuBarItems.byName('Meeting');
    isMeeting = meeting.exists();

    var muteItem = meeting.menus[0].menuItems.byName("Mute audio");
    audioStatus = muteItem.exists() ? "unmuted" : "muted";

    var videoItem = meeting.menus[0].menuItems.byName("Stop video");
    videoStatus = videoItem.exists() ? "unmuted" : "muted";
  }

  var json = JSON.stringify({"zoom": isZoom, "meeting": isMeeting, "audio":audioStatus, "video":videoStatus});
  console.log(json);

  if(!writeStateToFile(json)) {
    console.log(`could not write state file ${STATE_FILE}`);
  }
}

function writeStateToFile(text) {
    try {
        var openedFile = app.openForAccess(Path(STATE_FILE), { writePermission: true })
 
        app.setEof(openedFile, { to: 0 }) 
        app.write(text+"\n", { to: openedFile, startingAt: app.getEof(openedFile) })
        app.closeAccess(openedFile)
 
        return true
    }
    catch(error) { 
        try {
            app.closeAccess(file)
        }
        catch(error) {
            console.log(`Couldn't close file: ${error}`)
        }
 
        return false
    }
}


