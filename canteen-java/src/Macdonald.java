import javax.crypto.Mac;
import java.io.IOException;

public class Macdonald extends Stall{
    // compare to stall class, mac has bf menu
    private String bf_menu;

    public Macdonald(String stall_name,String operating_hours,String menu,int averageWaitingTime,String bf_menu) throws IOException {
        super(stall_name,operating_hours,menu,averageWaitingTime);
        this.bf_menu = bf_menu;
    }

    /*
     since Macdonald has breakfast menu and normal menu
     this method can help to get correct menu based on the current time
     */
    public String get_correct_menu(int hour){
        String mac_OH = this.getOperating_hours();
        String mac_OH_bf = mac_OH.split("\n")[1];
        String mac_bf_time = (mac_OH_bf.split(":")[1]).replace("am","").replace("pm","");
        int mac_bf_hour_start = Integer.parseInt(mac_bf_time.split("-")[0]);
        int mac_bf_hour_end = Integer.parseInt(mac_bf_time.split("-")[1]);

        if(hour >= mac_bf_hour_start && hour < mac_bf_hour_end){
            return this.bf_menu;
        }
        else{
            return this.get_menu();
        }
    }


}
