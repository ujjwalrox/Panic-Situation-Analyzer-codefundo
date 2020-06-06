package com.example.daksh.jsonparsing;

import android.annotation.SuppressLint;
import android.content.Context;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Handler;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.view.textclassifier.TextClassification;
import android.widget.Button;
import android.widget.TextView;

import com.android.volley.Cache;
import com.android.volley.Network;
import com.android.volley.NetworkResponse;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.BasicNetwork;
import com.android.volley.toolbox.DiskBasedCache;
import com.android.volley.toolbox.HttpHeaderParser;
import com.android.volley.toolbox.HurlStack;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.apache.commons.codec.StringEncoder;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.BasicResponseHandler;
import org.apache.http.impl.client.DefaultHttpClient;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedOutputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.io.UnsupportedEncodingException;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.concurrent.Executor;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

public class MainActivity extends AppCompatActivity {

    private TextView mTextViewResult;
    private RequestQueue mQueue;
    private Runnable runnable;
    private ScheduledExecutorService scheduler;
    public static Context mContext;


    public final static String username = "Daksh";
    public final static String longitude = "78.5695571899414";
    public final static String latitude = "17.546300888061523";
    public final static String url = "http://172.16.224.224:8000/api/location/";


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        mContext = getApplicationContext();

        mTextViewResult = (TextView)findViewById(R.id.textView);
        Button butttonParse = (Button)findViewById(R.id.button_parse);
        Button buttonSendRequest = (Button)findViewById(R.id.button_send_response);

        mQueue  = Volley.newRequestQueue(mContext);

        butttonParse.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                jsonParse();
            }
        });

        buttonSendRequest.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                sendDataToServer();
            }
        });

        ScheduledExecutorService scheduler = Executors.newScheduledThreadPool(1);

        final Runnable [] runnables = new Runnable[1];

        // Create the Handler
        final Handler handler = new Handler();

        // Define the code block to be executed
        final Runnable runnable = new Runnable(){
            @Override
            public void run() {
                // Insert custom code here
                startService(new Intent(mContext, YourService.class));
                // Repeat every 2 seconds
                handler.postDelayed(runnables[0], 5000);
            }
        };

        scheduler.scheduleAtFixedRate(runnable, 8, 8, TimeUnit.SECONDS);

    }

    private void jsonParse(){

        String url = "https://api.myjson.com/bins/kp9wz";

        JsonObjectRequest request = new JsonObjectRequest(Request.Method.GET, url, null,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        try {
                            JSONArray jsonArray = response.getJSONArray("employees");

                            for(int i=0; i<jsonArray.length(); i++){
                                JSONObject employee = jsonArray.getJSONObject(i);

                                String firstName = employee.getString("firstname");
                                int age = employee.getInt("age");
                                String mail = employee.getString("mail");

                                mTextViewResult.append(firstName + ", " + age + ", " + mail
                                        + "\n\n" );

                            }

                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }
                }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                error.printStackTrace();
            }
        });

        mQueue.add(request);

    }


    private static Map<String, String> checkParams(Map<String, String> map){
        Iterator<Map.Entry<String, String>> it = map.entrySet().iterator();
        while (it.hasNext()) {
            Map.Entry<String, String> pairs = (Map.Entry<String, String>)it.next();
            if(pairs.getValue()==null){
                map.put(pairs.getKey(), "");
            }
        }
        return map;
    }

    @SuppressLint("StaticFieldLeak")
    public void sendDataToServer(){


        new AsyncCaller().execute();

    }

    public static void getServerResponse(Map<String,String> json){

        final Map<String, String> json_value= json;

        RequestQueue queue = MySingleton.getInstance(mContext.getApplicationContext()).
                getRequestQueue();


        StringRequest MyStringRequest = new StringRequest(Request.Method.POST, url, new Response.Listener<String>() {
            @Override
            public void onResponse(String response) {

            }
        }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {

            }
        }){
            @Override
            protected Map<String, String> getParams() {
                return checkParams(json_value);
            }
        };


        MySingleton.getInstance(mContext).addToRequestQueue(MyStringRequest);
    }
}



