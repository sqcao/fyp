import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;

public class Stall {
    private String stall_name;
    private String operating_hours;
    private String menu;
    private int averageWaitingTime;

    // getter
    public String getStall_name(){
        return this.stall_name;
    }
    public  String getOperating_hours(){
        return this.operating_hours;
    }
    public String get_menu(){
        return this.menu;
    }
    public int getAverageWaitingTime(){
        return this.averageWaitingTime;
    }

    // setter
    public void setStall_name(String stall_name){
        this.stall_name = stall_name;
    }
    public void setOperating_hours(String operating_hours){
        this.operating_hours = operating_hours;
    }
    public void setMenu(String menu){
        this.menu = menu;
    }
    public void setAverageWaitingTime(int averageWaitingTime){
        this.averageWaitingTime = averageWaitingTime;
    }

    // empty constructor for getting the ref
    public Stall(){

    }

    // constructor
    public Stall(String stall_name,String operating_hours,String menu,int averageWaitingTime) throws IOException {
        this.stall_name = stall_name;
        this.operating_hours = operating_hours;
        this.menu = menu;
        this.averageWaitingTime = averageWaitingTime;
}


    public int calculateWaitTime(String numPeople){
        int number_people = Integer.parseInt(numPeople);
        return this.averageWaitingTime*number_people;
    }

    // check whether the store is open on one day with given time_str
    public boolean isOpening(String day_str,int hour){
        // get today's day in a week
        String[] weekday = new String[]{"Monday","Tuesday","Wedsday","Thursday","Friday"};
        boolean isWeekday = Arrays.stream(weekday).anyMatch(day_str::equals);

        String whole_OH = this.operating_hours;
        ArrayList<String> whole_OH_arraylist = new ArrayList();
        // get all the lines in text file that belongs to the current checking stall
        String[] whole_OH_array = whole_OH.split("\n");
        for(int i=0;i<whole_OH_array.length;i++){
            if(!whole_OH_array[i].equals("null")){
                whole_OH_arraylist.add(whole_OH_array[i]);
            }
        }

        // get all weekday opening stalls
        if(isWeekday){
            // if stall provides breakfast, then there will be 5 lines in the text file
            if(whole_OH_arraylist.size() == 5){
                String weekday_OH_str = (whole_OH_arraylist.get(3)).split(":")[1];
                String weekday_OH = weekday_OH_str.replace("am","").replace("pm","");
                int open_hr = Integer.parseInt(weekday_OH.split("-")[0]);
                int close_hr = Integer.parseInt(weekday_OH.split("-")[1]);
                if(hour >= open_hr && hour < close_hr){
                    return true;
                }
                else{
                    return false;
                }
            }
            // if the stall does not provide breakfast, then only 4 lines in the text file
            else{
                String weekday_OH_str = (whole_OH_arraylist.get(2)).split(":")[1];
                String weekday_OH = weekday_OH_str.replace("am","").replace("pm","");
                int open_hr = Integer.parseInt(weekday_OH.split("-")[0]);
                int close_hr = Integer.parseInt(weekday_OH.split("-")[1]);
                if(hour >= open_hr && hour < close_hr){
                    return true;
                }
                else{
                    return false;
                }
            }
        }
        // get all saturday opening stalls
        else if(day_str.equals("Saturday")){
            if(whole_OH_arraylist.size() == 5){ // provide breakfast
                String saturday_OH_str = (whole_OH_arraylist.get(3)).split(":")[1];

                String saturday_OH = saturday_OH_str.replace("am","").replace("pm","");
                int open_hr = Integer.parseInt(saturday_OH.split("-")[0]);
                int close_hr = Integer.parseInt(saturday_OH.split("-")[1]);

                if(hour >= open_hr && hour < close_hr){
                    return true;
                }
                else{
                    return false;
                }
            }
            else{   // no breakfast
                String saturday_OH_str = (whole_OH_arraylist.get(2)).split(":")[1];
                String saturday_OH = saturday_OH_str.replace("am","").replace("pm","");
                int open_hr = Integer.parseInt(saturday_OH.split("-")[0]);
                int close_hr = Integer.parseInt(saturday_OH.split("-")[1]);

                if(hour >= open_hr && hour < close_hr){
                    return true;
                }
                else{
                    return false;
                }
            }
        }
        // get all sunday opening stalls
        else{
            if(whole_OH_arraylist.size() == 5){ // provide breakfast
                String sunday_OH_str = (whole_OH_arraylist.get(4)).split(":")[1];
                if(sunday_OH_str.equals("closed")){
                    System.out.println(this.stall_name + " closed");
                    return false;
                }
                String sunday_OH = sunday_OH_str.replace("am","").replace("pm","");
                int open_hr = Integer.parseInt(sunday_OH.split("-")[0]);
                int close_hr = Integer.parseInt(sunday_OH.split("-")[1]);
                if(hour >= open_hr && hour < close_hr){
                    return true;
                }
                else{
                    return false;
                }
            }
            else{   // no breakfast
                String sunday_OH_str = (whole_OH_arraylist.get(3)).split(":")[1];
                if(sunday_OH_str.equals("closed")){
                    System.out.println(this.stall_name + " closed");
                    return false;
                }
                String sunday_OH = sunday_OH_str.replace("am","").replace("pm","");
                int open_hr = Integer.parseInt(sunday_OH.split("-")[0]);
                int close_hr = Integer.parseInt(sunday_OH.split("-")[1]);
                if(hour >= open_hr && hour < close_hr){
                    return true;
                }
                else{
                    return false;
                }
            }
        }

    }



}
