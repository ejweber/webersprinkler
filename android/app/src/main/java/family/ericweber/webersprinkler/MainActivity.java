package family.ericweber.webersprinkler;

import android.app.Activity;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.widget.TextView;

import com.google.gson.Gson;

import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLConnection;
import java.util.List;

public class MainActivity extends Activity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Status status = new Status();
        (new GetStatus()).execute(status);
    }

    private class GetStatus extends AsyncTask<MainActivity.Status, Integer, MainActivity.Status> {
        @Override
        protected MainActivity.Status doInBackground(MainActivity.Status... statusArray) {
            MainActivity.Status status = statusArray[0];
            try {
                URL statusURL = new URL("http", "ericweber.family", 5002, "/api/status");
                HttpURLConnection statusConnection = (HttpURLConnection) statusURL.openConnection();
                InputStreamReader statusReader = new InputStreamReader(statusConnection.getInputStream());
                Gson statusGson = new Gson();
                status = statusGson.fromJson(statusReader, MainActivity.Status.class);
                statusConnection.disconnect();
                status.debugLog();
            } catch (MalformedURLException e) {
                Log.w("Exception", "MalformedURLException");
            } catch (java.io.IOException e) {
                Log.w("Exception", "IOException");
            }
        return status;
        }

        @Override
        protected void onPostExecute(MainActivity.Status status) {
            ((TextView)findViewById(R.id.status)).setText("Ready");
            ((TextView)findViewById(R.id.zone)).setText(status.zone);
            ((TextView)findViewById(R.id.program)).setText(status.program);
            ((TextView)findViewById(R.id.remaining)).setText(status.time);
            ((TextView)findViewById(R.id.nextTime)).setText(status.next.run_time);
            ((TextView)findViewById(R.id.nextProgram)).setText(status.next.name);
        }
    }

    private class Status {
        private String time;
        private String zone;
        private String program;
        private NextProgram next;

        private class NextProgram {
            private String run_time;
            private String name;
        }

        private void debugLog() {
            String debugMessage = "time: " + time + '\n' +
                                  "zone: " + zone + '\n' +
                                  "program: " + program + '\n' +
                                  "next: " + '\n' +
                                  "\trun_time: " + next.run_time + '\n' +
                                  "\tname: " + next.name;
            Log.d("Status", debugMessage);
        }
    }
}

