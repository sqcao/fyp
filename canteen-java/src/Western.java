import java.io.IOException;

public class Western extends Stall{

    private String bf_menu;

    public Western(String stall_name,String operating_hours,String menu,int averageWaitingTime,String bf_menu) throws IOException {
        super(stall_name,operating_hours,menu,averageWaitingTime);
        this.bf_menu = bf_menu;
    }

    /*
     since western stall has breakfast menu and normal menu
     this method can help to get correct menu based on the current time
     */
    public String get_correct_menu(int hour){
        String western_OH = this.getOperating_hours();
        System.out.println(western_OH);
        String western_OH_bf = western_OH.split("\n")[2];
        System.out.println(western_OH_bf);
        String western_bf_time = (western_OH_bf.split(":")[1]).replace("am","").replace("pm","");
        int western_bf_hour_start = Integer.parseInt(western_bf_time.split("-")[0]);
        int western_bf_hour_end = Integer.parseInt(western_bf_time.split("-")[1]);

        if(hour >= western_bf_hour_start && hour < western_bf_hour_end){
            return this.bf_menu;
        }
        else{
            return this.get_menu();
        }
    }


}
