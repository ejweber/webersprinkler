package family.ericweber.webersprinkler.Fragments;

import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.NumberPicker;
import android.widget.Spinner;
import android.widget.TextView;

import family.ericweber.webersprinkler.Library.RestReturnPrograms;
import family.ericweber.webersprinkler.Library.RestReturnStatus;
import family.ericweber.webersprinkler.R;
import family.ericweber.webersprinkler.RestClasses.RestProgram;
import family.ericweber.webersprinkler.RestClasses.RestStatus;

public class StatusAndControl extends Fragment {

    private ArrayAdapter<RestProgram> programAdapter;
    private StatusCallback statusCallback = new StatusCallback();
    private ProgramsCallback programsCallback = new ProgramsCallback();

    public StatusAndControl() {
        // Required empty public constructor
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // programAdapter setup
        programAdapter = new ArrayAdapter<>(getContext(),
                android.R.layout.simple_spinner_item);
        programAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        (new RestReturnPrograms(programsCallback)).execute();
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_status_and_control, container, false);
    }

    @Override
    public void onViewCreated(final View fragmentView, Bundle savedInstanceState) {

        (new RestReturnStatus(statusCallback)).execute();

        // zoneSpinner setup
        final Spinner zoneSpinner = fragmentView.findViewById(R.id.zoneSpinner);
        ArrayAdapter<CharSequence> zoneAdapter = ArrayAdapter.createFromResource(getContext(),
                R.array.zones_array, android.R.layout.simple_spinner_item);
        zoneAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        zoneSpinner.setAdapter(zoneAdapter);

        // timePicker setup
        final NumberPicker timePicker = fragmentView.findViewById(R.id.zoneTimePicker);
        timePicker.setMaxValue(60);
        timePicker.setMinValue(0);
        timePicker.setWrapSelectorWheel(false);

        // zoneButton setup
        Button zoneButton = fragmentView.findViewById(R.id.zoneButton);
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
                (new RestReturnStatus("post", endpoint, statusCallback)).execute();
            }
        });

        // programSpinner setup
        final Spinner programSpinner = fragmentView.findViewById(R.id.programSpinner);
        programSpinner.setAdapter(programAdapter);

        // programButton setup
        Button programButton = fragmentView.findViewById(R.id.programButton);
        programButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                RestProgram program = (RestProgram) programSpinner.getSelectedItem();
                String endpoint = "/api/run/program" + program.getId();
                (new RestReturnStatus("post", endpoint, statusCallback)).execute();
            }
        });

        // refreshButton setup
        Button refreshButton = fragmentView.findViewById(R.id.refreshButton);
        refreshButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                (new RestReturnStatus(statusCallback)).execute();
            }
        });

        // stopButton setup
        Button stopButton = fragmentView.findViewById(R.id.stopButton);
        stopButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                (new RestReturnStatus("post", "api/stop",
                        statusCallback)).execute();
            }
        });
    }

    @Override
    public void onDetach() {
        super.onDetach();
    }

    private class StatusCallback implements RestReturnStatus.StatusListener {

        @Override
        public void onReturnStatus(RestStatus status) {
            View view = getView();
            if (view != null) {
                if (status.getZone() == null) {
                    ((TextView) view.findViewById(R.id.currentStatus)).setText(R.string.ready);
                } else {
                    ((TextView) view.findViewById(R.id.currentStatus)).setText(R.string.running);
                }
                ((TextView) view.findViewById(R.id.currentProgram)).setText(status.getProgram());
                ((TextView) view.findViewById(R.id.currentZone)).setText(status.getZone());
                ((TextView) view.findViewById(R.id.currentTimeLeft)).setText(status.getTime());
                ((TextView) view.findViewById(R.id.nextProgram)).setText(status.getNextName());
                ((TextView) view.findViewById(R.id.nextTime)).setText(status.getNextTime());
            }
        }
    }

    private class ProgramsCallback implements RestReturnPrograms.ProgramListener {

        @Override
        public void onReturnPrograms(RestProgram[] programs) {
            programAdapter.clear();
            programAdapter.addAll(programs);
        }
    }
}
