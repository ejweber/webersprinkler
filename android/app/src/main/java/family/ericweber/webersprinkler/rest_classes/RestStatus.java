package family.ericweber.webersprinkler.rest_classes;

import android.util.Log;

public class RestStatus {
    private String time;
    private String zone;
    private String program;
    private NextProgram next;

    private class NextProgram {
        private String run_time;
        private String name;
    }

    public String getTime() {return time;};
    public String getZone() {return zone;};
    public String getProgram() {return program;};
    public String getNextName() {return next.name;};
    public String getNextTime() {return next.run_time;};

    public void debugLog() {
        String debugMessage = "time: " + time + '\n' +
                "zone: " + zone + '\n' +
                "program: " + program + '\n' +
                "next: " + '\n' +
                "\trun_time: " + next.run_time + '\n' +
                "\tname: " + next.name;
        Log.d("Status", debugMessage);
    }
}
