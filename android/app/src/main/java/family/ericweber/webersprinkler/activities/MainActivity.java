package family.ericweber.webersprinkler.activities;

import android.app.Activity;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.widget.TextView;

import com.google.gson.Gson;

import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;

import family.ericweber.webersprinkler.R;
import family.ericweber.webersprinkler.rest_classes.RestStatus;

public class MainActivity extends Activity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        RestStatus status = new RestStatus();
        (new GetStatus()).execute(status);
    }

    private class GetStatus extends AsyncTask<RestStatus, Integer, RestStatus> {
        @Override
        protected RestStatus doInBackground(RestStatus... statusArray) {
            RestStatus status = statusArray[0];
            try {
                URL statusURL = new URL("http", "ericweber.family", 5002, "/api/status");
                HttpURLConnection statusConnection = (HttpURLConnection) statusURL.openConnection();
                InputStreamReader statusReader = new InputStreamReader(statusConnection.getInputStream());
                Gson statusGson = new Gson();
                status = statusGson.fromJson(statusReader, RestStatus.class);
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
        protected void onPostExecute(RestStatus status) {
            ((TextView)findViewById(R.id.status)).setText("Ready");
            ((TextView)findViewById(R.id.zone)).setText(status.getZone());
            ((TextView)findViewById(R.id.program)).setText(status.getProgram());
            ((TextView)findViewById(R.id.remaining)).setText(status.getTime());
            ((TextView)findViewById(R.id.nextTime)).setText(status.getNextTime());
            ((TextView)findViewById(R.id.nextProgram)).setText(status.getNextName());
        }
    }
}

