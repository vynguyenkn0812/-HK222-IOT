package BK.HK222.IoT.dashboardiot;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.Bundle;
import android.util.Base64;
import android.util.Log;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.ListView;
import android.widget.TextView;

import com.github.angads25.toggle.interfaces.OnToggledListener;
import com.github.angads25.toggle.model.ToggleableView;
import com.github.angads25.toggle.widget.LabeledSwitch;

import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallbackExtended;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.eclipse.paho.client.mqttv3.MqttException;

import java.nio.charset.Charset;
import java.util.ArrayList;

public class MainActivity extends AppCompatActivity {
    private final String TAG = getClass().getSimpleName();



    MQTTHelper mqttHelper;
    TextView txtTemp, txtHumi, txtBright;
    LabeledSwitch tgLight, tgPump;
    ListView list;
    ArrayAdapter<String> adapter;
    ArrayList<String> arrayList;
    ImageView imageAI;
    String sImage;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        txtTemp = findViewById(R.id.txtTemperature);
        txtHumi = findViewById(R.id.txtHumidity);
        txtBright = findViewById(R.id.txtBrightness);
        tgLight = findViewById(R.id.toggleLight);
        tgPump = findViewById(R.id.togglePump);
        list = findViewById(R.id.listEmployee);
        imageAI = findViewById(R.id.imgAI);
        arrayList = new ArrayList<String>();
        adapter = new ArrayAdapter<String>(getApplicationContext(), android.R.layout.simple_spinner_item, arrayList);
        list.setAdapter(adapter);


        tgLight.setOnToggledListener(new OnToggledListener() {
            @Override
            public void onSwitched(ToggleableView toggleableView, boolean isOn) {
                if (isOn == true) {
                    sendDataMQTT("vynguyen08122002/feeds/iot-hk222.light", "1");
                } else if (isOn == false) {
                    sendDataMQTT("vynguyen08122002/feeds/iot-hk222.light", "0");
                }
            }
        });

        tgPump.setOnToggledListener(new OnToggledListener() {
            @Override
            public void onSwitched(ToggleableView toggleableView, boolean isOn) {
                if (isOn == true) {
                    sendDataMQTT("vynguyen08122002/feeds/iot-hk222.pump", "1");
                } else if (isOn == false) {
                    sendDataMQTT("vynguyen08122002/feeds/iot-hk222.pump", "0");
                }
            }
        });


        startMQTT();
    }

    @Override
    protected void onStart() {
        super.onStart();
        Log.d(TAG, "onStart: ");
    }

    @Override
    protected void onResume() {
        super.onResume();
        Log.d(TAG, "onResume: ");
    }

    @Override
    protected void onPause() {
        super.onPause();
        Log.d(TAG, "onPause: ");
    }
    
    @Override
    protected void onStop() {
        super.onStop();
        Log.d(TAG, "onStop: ");
    }
    
    @Override
    protected void onDestroy() {
        super.onDestroy();
        Log.d(TAG, "onDestroy: ");
    }

    public void sendDataMQTT(String topic, String value){
        MqttMessage msg = new MqttMessage();
        msg.setId(1234);
        msg.setQos(0);
        msg.setRetained(false);

        byte[] b = value.getBytes(Charset.forName("UTF-8"));
        msg.setPayload(b);

        try {
            mqttHelper.mqttAndroidClient.publish(topic, msg);
        } catch (MqttException e){
        }
    }

    public void startMQTT() {
        mqttHelper = new MQTTHelper(this);
        mqttHelper.setCallback(new MqttCallbackExtended() {
            @Override
            public void connectComplete(boolean reconnect, String serverURI) {

            }

            @Override
            public void connectionLost(Throwable cause) {

            }

            @Override
            public void messageArrived(String topic, MqttMessage message) throws Exception {
                Log.d("TEST", topic + "***" + message.toString());
                if (topic.contains("iot-hk222.temperature")) {
                    txtTemp.setText(message.toString() + " ℃");
                } else if (topic.contains("iot-hk222.humidity")) {
                    txtHumi.setText(message.toString() + " %");
                } else if (topic.contains("iot-hk222.brightness")) {
                    txtBright.setText(message.toString() + " lux");
                } else if (topic.contains("iot-hk222.light")) {
                    if (message.toString().equals("1")) {
                        tgLight.setOn(true);
                    } else if (message.toString().equals("0")) {
                        tgLight.setOn(false);
                    }
                } else if (topic.contains("iot-hk222.pump")) {
                    if (message.toString().equals("1")) {
                        tgPump.setOn(true);
                    } else if (message.toString().equals("0")) {
                        tgPump.setOn(false);
                    }
                } else if (topic.contains("iot-hk222.ai")) {
                    arrayList.add(message.toString());
                    // next thing you have to do is check if your adapter has changed
                    adapter.notifyDataSetChanged();
                } else if (topic.contains("iot-hk222.ai-image-recognize")) {
                    // Decode base64 String
                    sImage = message.toString();
                    Log.d(TAG, "messageArrived: " + sImage);
                    byte[] bytes = Base64.decode(sImage, Base64.DEFAULT);

                    // Initialize bitmap
                    Bitmap bitmap = BitmapFactory.decodeByteArray(bytes, 0, bytes.length);

                    // Set bitmap on image view
                    imageAI.setImageBitmap(bitmap);

                }
            }

            @Override
            public void deliveryComplete(IMqttDeliveryToken token) {

            }
        });
    }
}