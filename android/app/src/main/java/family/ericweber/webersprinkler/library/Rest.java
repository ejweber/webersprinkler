package family.ericweber.webersprinkler.library;

import com.google.gson.Gson;

import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;

public class Rest<Input, Output> {

    private URL endpoint;
    private Class<Output> outputClass;

    public Rest(String endpoint, Class<Output> cls) {
        try {
            this.endpoint = new URL("http", "ericweber.family", 5002, endpoint);
        }
        catch (MalformedURLException e) {
            throw new Error("malformed URL exception");
        }
        outputClass = cls;
    }

    public Output Get() {
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
        Output outputObject = (new Gson()).fromJson(stream, outputClass);
        connection.disconnect();
        return outputObject;
    }

    public Output Post() {
        // the () typecasts a URLConnection to an HttpURLConnection
        HttpURLConnection connection;
        InputStreamReader stream;
        try {
            connection = (HttpURLConnection) endpoint.openConnection();
            connection.setDoOutput(true);
            stream = new InputStreamReader(connection.getInputStream());
        }
        catch (IOException e) {
            throw new Error("IO exception!");
        }
        Output outputObject = (new Gson()).fromJson(stream, outputClass);
        connection.disconnect();
        return outputObject;
    }
}