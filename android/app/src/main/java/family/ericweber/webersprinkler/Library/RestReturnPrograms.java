package family.ericweber.webersprinkler.Library;

import android.os.AsyncTask;
import android.util.Log;

import family.ericweber.webersprinkler.RestClasses.RestProgram;

public class RestReturnPrograms extends AsyncTask<Void, Void, RestProgram[]> {
    private ProgramListener listener;
    private String requestType;
    private String endpoint;
    private RestProgram outputProgram;

    public RestReturnPrograms(ProgramListener listener) {
        this.listener = listener;
        this.requestType = "get";
        this.endpoint = "/api/programs";
    }

    public RestReturnPrograms(RestProgram program, ProgramListener listener) {
        this.listener = listener;
        this.requestType = "post";
        this.endpoint = "/api/programs/" + String.valueOf(program.getId());
        this.outputProgram = program;
    }

    @Override
    protected RestProgram[] doInBackground(Void... params) {
        RestProgram[] programs = null;
        switch (requestType) {
            case "get":
                programs =  (new Rest<Void, RestProgram[]>(endpoint, RestProgram[].class)).Get();
                break;
            case "post":
                Log.d("endpoint", endpoint);
                programs = (new Rest<>(endpoint, outputProgram, RestProgram.class, RestProgram[].class)).Post();
                break;
        }
        return programs;
    }

    @Override
    protected void onPostExecute(RestProgram[] programs) {
        listener.onReturnPrograms(programs);
    }

    public interface ProgramListener {
        void onReturnPrograms(RestProgram[] programs);
    }
}