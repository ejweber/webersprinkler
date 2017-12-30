package family.ericweber.webersprinkler.activities;

import android.app.Activity;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.NumberPicker;
import android.widget.Spinner;
import android.widget.TextView;

import family.ericweber.webersprinkler.R;
import family.ericweber.webersprinkler.library.Rest;
import family.ericweber.webersprinkler.rest_classes.RestProgram;
import family.ericweber.webersprinkler.rest_classes.RestStatus;

public class MainActivity extends Activity {

    private RestProgram[] programList;
    private ArrayAdapter<RestProgram> programAdapter;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        (new GetStatus()).execute();
        (new GetPrograms()).execute();

        // zoneSpinner setup
        final Spinner zoneSpinner = findViewById(R.id.zoneSpinner);
        ArrayAdapter<CharSequence> zoneAdapter = ArrayAdapter.createFromResource(this,
                R.array.zones_array, android.R.layout.simple_spinner_item);
        zoneAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        zoneSpinner.setAdapter(zoneAdapter);

        // timePicker setup
        final NumberPicker timePicker = findViewById(R.id.zoneTimePicker);
        timePicker.setMaxValue(60);
        timePicker.setMinValue(0);
        timePicker.setWrapSelectorWheel(false);

        // zoneButton setup
        Button zoneButton = findViewById(R.id.zoneButton);
        zoneButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                String zoneString = (String) zoneSpinner.getSelectedItem();
                char zoneChar = zoneString.charAt(zoneString.length() - 1);
                String endpoint = "/api/run/manual/" + zoneChar;
                int zoneTime = timePicker.getValue();
                if (zoneTime != 0) {
                    endpoint = endpoint + '/' + zoneTime;
                }
                Log.d("Main Activity", endpoint);
                (new PostReturnStatus()).execute(endpoint);
            }
        });

        // programSpinner setup
        final Spinner programSpinner = findViewById(R.id.programSpinner);
        programAdapter = new ArrayAdapter<>(this,
                android.R.layout.simple_spinner_item);
        programAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        programSpinner.setAdapter(programAdapter);

        // programButton setup
        Button programButton = findViewById(R.id.programButton);
        programButton.setOnClickListener(new View.OnClickListener() {
           @Override
            public void onClick (View view) {
               RestProgram program = (RestProgram) programSpinner.getSelectedItem();
               (new PostReturnStatus()).execute("/api/run/program/" + program.getId());
           }
        });

        // refreshButton setup
        Button refreshButton = findViewById(R.id.refreshButton);
        refreshButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                (new GetStatus()).execute();
            }
        });

        // stopButton setup
        Button stopButton = findViewById(R.id.stopButton);
        stopButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                (new PostReturnStatus()).execute("api/stop");
            }
        });
    }

    private class GetStatus extends AsyncTask<Void, Void, RestStatus> {
        @Override
        protected RestStatus doInBackground(Void... statusArray) {
            return (new Rest<Void, RestStatus>("api/status", RestStatus.class).Get());
        }

        @Override
        protected void onPostExecute(RestStatus status) {
            if (status.getZone() == null) {
                ((TextView) findViewById(R.id.status)).setText("Ready");
            }
            else {
                ((TextView) findViewById(R.id.status)).setText("Running");
            }
            ((TextView)findViewById(R.id.zone)).setText(status.getZone());
            ((TextView)findViewById(R.id.program)).setText(status.getProgram());
            ((TextView)findViewById(R.id.remaining)).setText(status.getTime());
            ((TextView)findViewById(R.id.nextTime)).setText(status.getNextTime());
            ((TextView)findViewById(R.id.nextProgram)).setText(status.getNextName());
        }
    }

    private class PostReturnStatus extends AsyncTask<String, Void, RestStatus> {
        @Override
        protected RestStatus doInBackground(String... endpointArray) {
            return (new Rest<Void, RestStatus>(endpointArray[0], RestStatus.class).Post());
        }

        @Override
        protected void onPostExecute(RestStatus status) {
            if (status.getZone() == null) {
                ((TextView) findViewById(R.id.status)).setText("Ready");
            }
            else {
                ((TextView) findViewById(R.id.status)).setText("Running");
            }
            ((TextView)findViewById(R.id.zone)).setText(status.getZone());
            ((TextView)findViewById(R.id.program)).setText(status.getProgram());
            ((TextView)findViewById(R.id.remaining)).setText(status.getTime());
            ((TextView)findViewById(R.id.nextTime)).setText(status.getNextTime());
            ((TextView)findViewById(R.id.nextProgram)).setText(status.getNextName());
        }
    }

    private class GetPrograms extends AsyncTask<Void, Void, Void> {
        @Override
        protected Void doInBackground(Void... params) {
            programList = (new Rest<Void, RestProgram[]>(
                    "api/programs", RestProgram[].class).Get());
            return null;
        }

        @Override
        protected void onPostExecute(Void param) {
            programAdapter.clear();
            programAdapter.addAll(programList);
        }
    }
}

