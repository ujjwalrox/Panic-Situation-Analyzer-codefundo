package com.example.daksh.jsonparsing;

import android.os.AsyncTask;
import android.widget.Toast;

import java.util.HashMap;
import java.util.Map;

public class AsyncCaller extends AsyncTask<Void, Void, Void>{

    public final static String username = "Daksh";
    public final static String longitude = "78.5695571899414";
    public final static String latitude = "17.546300888061523";


    @Override
    protected Void doInBackground(Void... voids) {
        final Map<String, String> json = formatDataAsJSON();
        MainActivity.getServerResponse(json);
        return null;
    }

    @Override
    protected void onPostExecute(Void aVoid) {
        super.onPostExecute(aVoid);
    }

    private Map<String, String> formatDataAsJSON(){

        Map<String, String> params = new HashMap<String, String>();
        params.put("username", username);
        params.put("lng", longitude);
        params.put("lat", latitude);
        return params;

    }
}
