package family.ericweber.webersprinkler.rest_classes;

public class RestProgram {

    private String name;
    private String description;
    private String id;
    private boolean recurring;
    // TODO: figure out how to dynamically allocate the right size of array
    private String[] run_times = new String[3];
    private int[] zone_times = new int[5];

    public String getName() {return name;}
    public String getDescription() {return description;}
    public boolean getRecurring() {return recurring;}
    public String getId() {return id;};
    public String[] getRunTimes() {return run_times;}
    public int[] getZoneTimes() {return zone_times;}

    public String toString() {return getName();}
}
