package family.ericweber.webersprinkler.Library;

import android.util.Log;

import com.google.gson.Gson;

import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;

public class Rest<Output, Input> {
    static int port = 5001;
    private URL endpoint;
    private Output outputObject;
    private Class<Output> outputClass;
    private Class<Input> inputClass;

    public Rest(String endpoint, Class<Input> inputClass) {
        try {
            this.endpoint = new URL("http", "ericweber.family", port, endpoint);
        }
        catch (MalformedURLException e) {
            throw new Error("malformed URL exception");
        }
        this.outputObject = null;
        this.outputClass = null;
        this.inputClass = inputClass;
        Log.d("endpoint", this.endpoint.toString());
    }

    public Rest(String endpoint, Output outputObject, Class<Output> outputClass, Class<Input> inputClass) {
        try {
            this.endpoint = new URL("http", "ericweber.family", port, endpoint);
        }
        catch (MalformedURLException e) {
            throw new Error("malformed URL exception");
        }
        this.outputObject = outputObject;
        this.outputClass = outputClass;
        this.inputClass = inputClass;
    }


    public Input Get() {
        // the () typecasts a URLConnection to an HttpURLConnection
        HttpURLConnection connection;
        InputStreamReader stream;
        try {
            connection = (HttpURLConnection) endpoint.openConnection();
            stream = new InputStreamReader(connection.getInputStream());
        }
        catch (IOException e) {
            throw new Error("IO exception!");
        }
        Input inputObject = (new Gson()).fromJson(stream, inputClass);
        connection.disconnect();
        return inputObject;
    }

    public Input Post() {
        // the () typecasts a URLConnection to an HttpURLConnection
        HttpURLConnection connection;
        InputStreamReader inputStream;
        OutputStreamWriter outputStream;
        Input inputObject;
        try {
            connection = (HttpURLConnection) endpoint.openConnection();
            if (outputObject != null) {
                connection.setDoOutput(true);
                connection.setRequestProperty("Content-Type", "application/json");
                String outputString = (new Gson()).toJson(outputObject, outputClass);
                Log.d("outputString", outputString);
                outputStream = new OutputStreamWriter(connection.getOutputStream());
                outputStream.write(outputString);
                outputStream.flush();
                int responseCode = connection.getResponseCode();
                Log.d("Response code", String.valueOf(responseCode));
            }
            else {
                connection.setRequestMethod("POST");
            }
            inputStream = new InputStreamReader(connection.getInputStream());
            inputObject = (new Gson()).fromJson(inputStream, inputClass);
        }
        catch (IOException e) {
            throw new Error("IO exception!");
        }
        connection.disconnect();
        return inputObject;
    }
}