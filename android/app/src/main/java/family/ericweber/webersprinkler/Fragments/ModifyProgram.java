package family.ericweber.webersprinkler.Fragments;

import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.Spinner;

import family.ericweber.webersprinkler.Library.RestReturnPrograms;
import family.ericweber.webersprinkler.R;
import family.ericweber.webersprinkler.RestClasses.RestProgram;

public class ModifyProgram extends Fragment {
    private ProgramsCallback programsCallback = new ProgramsCallback();
    private SpinnerCallback spinnerCallback = new SpinnerCallback();
    private ArrayAdapter<String> runTimeAdapter;
    private ArrayAdapter<RestProgram> programAdapter;

    public ModifyProgram() {
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

        // runTimeAdapter setup
        runTimeAdapter = new ArrayAdapter<>(getContext(), android.R.layout.simple_list_item_1);
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_modify_program, container, false);
    }

    @Override
    public void onViewCreated(final View fragmentView, Bundle savedInstanceState) {
        // programSpinner setup
        final Spinner programSpinner = fragmentView.findViewById(R.id.programSpinner);
        programSpinner.setAdapter(programAdapter);
        programSpinner.setOnItemSelectedListener(spinnerCallback);

        // runTimeView setup
        final ListView runTimeView = fragmentView.findViewById(R.id.runTimeView);
        runTimeView.setAdapter(runTimeAdapter);
        runTimeView.setOnItemLongClickListener(new android.widget.AdapterView.OnItemLongClickListener() {
            @Override
            public boolean onItemLongClick(AdapterView parent, View view, int position, long id) {
                runTimeAdapter.remove((String)runTimeView.getItemAtPosition(position));
                return true;
            }
        });

        // modifyButton setup
        Button modifyButton = fragmentView.findViewById(R.id.modifyButton);
        modifyButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                RestProgram program = (RestProgram)programSpinner.getSelectedItem();
                (new RestReturnPrograms(program, programsCallback)).execute();
            }
        });
    }

    public void updateProgramView(RestProgram program) {
        Log.d("Timeline", "updateProgramView() called");
        View view = getView();
        if (view != null) {
            ((EditText) view.findViewById(R.id.program_name)).setText(program.getName());
            int id = 0;
            int[] zoneTimes = program.getZoneTimes();
            for (int i = 0; i < zoneTimes.length; i++) {
                switch (i) {
                    case 0:
                        id = R.id.time_0;
                        break;
                    case 1:
                        id = R.id.time_1;
                        break;
                    case 2:
                        id = R.id.time_2;
                        break;
                    case 3:
                        id = R.id.time_3;
                        break;
                    case 4:
                        id = R.id.time_4;
                        break;
                }
                ((EditText) view.findViewById(id)).setText(String.valueOf(zoneTimes[i]));
            }
            runTimeAdapter.clear();
            runTimeAdapter.addAll(program.getRunTimes());
        }
    }

    private class ProgramsCallback implements RestReturnPrograms.ProgramListener {

        @Override
        public void onReturnPrograms(RestProgram[] programs) {
            programAdapter.clear();
            programAdapter.addAll(programs);
        }
    }

    private class SpinnerCallback implements AdapterView.OnItemSelectedListener {

        @Override
        public void onItemSelected(AdapterView<?> parent, View view, int pos, long id) {
            Log.d("Timeline", "onItemSelected() called");
            updateProgramView(programAdapter.getItem(pos));
        }

        public void onNothingSelected(AdapterView<?> parent) {
            // TODO: do something later?
        }
    }
}