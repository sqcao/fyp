import java.io.IOException;

public class Malay extends Stall {
//    String malay_OH = super.readOH("Malay");
//    String malay_alt_menu = super.readMenu("Malay-246");
//    String malay_normal_menu = super.readMenu("Malay-135");


    private String alt_menu;



    public Malay(String stall_name,String operating_hours,String menu,int averageWaitingTime,String alt_menu) throws IOException {
        super(stall_name,operating_hours,menu,averageWaitingTime);
        this.alt_menu = alt_menu;
    }

    /*
     since malay stall's menu is different on (mon, wed, fri) and (tue, thur, sat)
     this method can help to get correct menu based on the current day
     */
    public String get_correct_menu(String weekday){
        if(weekday.equals("Monday") || weekday.equals("Wedsday") || weekday.equals("Friday")){
            return this.alt_menu;
        }
        else{
            return this.get_menu();
        }
    }


}
