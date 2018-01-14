package family.ericweber.webersprinkler.Library;

import android.os.AsyncTask;
import android.util.Log;
import android.view.View;
import android.widget.TextView;

import java.lang.ref.WeakReference;

import family.ericweber.webersprinkler.R;
import family.ericweber.webersprinkler.RestClasses.RestStatus;

public class RestReturnStatus extends AsyncTask<Void, Void, RestStatus> {
    private StatusListener listener;
    private String requestType;
    private String endpoint;

    public RestReturnStatus(StatusListener listener) {
        this.requestType = "get";
        this.endpoint = "/api/status";
        this.listener = listener;
    }

    public RestReturnStatus(String requestType, String endpoint, StatusListener listener) {
        this.requestType = requestType;
        this.endpoint = endpoint;
        this.listener = listener;
    }

    @Override
    protected RestStatus doInBackground(Void... params) {
        RestStatus status = new RestStatus();
        switch (requestType) {
            case "get":
                status =  (new Rest<Void, RestStatus>(endpoint, RestStatus.class)).Get();
                break;
            case "post":
                status = (new Rest<Void, RestStatus>(endpoint, RestStatus.class)).Post();
                break;
        }
        return status;
    }

    @Override
    protected void onPostExecute(RestStatus status) {
        listener.onReturnStatus(status);
    }

    public interface StatusListener {
        void onReturnStatus(RestStatus status);
    }
}
