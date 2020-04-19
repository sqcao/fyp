import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.image.BufferedImage;
import java.io.*;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import java.util.Locale;
import javax.imageio.ImageIO;
import javax.swing.*;

// this gui is using cardlayout
public class TabDemo extends JPanel{
    final static String MACPANEL = "Macdonald";
    final static String SUBWAYPANEL = "Subway";
    final static String WESTERNPANEL = "Western Food";
    final static String MALAYPANEL = "Malay Food";
    final static String ChICKENRICEPANEL = "Chicken Rice";
    final static int extraWindowWidth = 500;

    // add component into the view menu page
    public void addComponentToPane(Container pane,Boolean mac,Boolean subway,Boolean western,Boolean malay,Boolean chickenRice,
                                   String macMenu, String subwayMenu, String westernMenu, String malayMenu, String chickenRiceMenu) throws IOException {
        JTabbedPane tabbedPane = new JTabbedPane();
        pane.setPreferredSize(new Dimension(700, 500));
        // Create the "cards" in the menu display page
        // card1 - Macdonald menu
        if(mac) {
            JPanel card1 = new JPanel() {
                public void paintComponent(Graphics g) {
                    // get the background image for macdonald menu card
                    ImageIcon img = new ImageIcon("src\\images\\mac1.jpg");
                    System.out.println(g.drawImage(img.getImage(), 0, 0, 700, 500, null));
                    super.paintComponent(g);
                }

                /*
                Make the panel wider than it really needs, so
                the window's wide enough for the tabs to stay
                in one row.
                 */
                public Dimension getPreferredSize() {
                    Dimension size = super.getPreferredSize();
                    size.width += extraWindowWidth;
                    return size;
                }
            };
            card1.setOpaque(false);
            card1.setLayout(null);
            String macMenu_new = macMenu.replace("null","");
            System.out.println(macMenu_new);
            JTextArea textArea = new JTextArea(3, 20);
            textArea.setText(macMenu_new);
            textArea.setWrapStyleWord(true);
            textArea.setLineWrap(true);
            textArea.setOpaque(false);
            textArea.setEditable(false);
            textArea.setFocusable(false);
            textArea.setBackground(UIManager.getColor("Label.background"));
            textArea.setFont(new Font("Forte", Font.BOLD, 18));
            textArea.setBorder(UIManager.getBorder("Label.border"));
            textArea.setBounds(50,50,200,400);
            card1.add(textArea);

            // add in the button to check waiting time and operating hour
            JButton waitTimeBt_card1 = new JButton("Wait Time");
            waitTimeBt_card1.addActionListener(new ActionListener() {
                @Override
                public void actionPerformed(ActionEvent e) {    // for pressing waitTime button
                    String numPeople = JOptionPane.showInputDialog(null, "please enter how many people in the queue:");
                /*
                 get mac average waiting time
                 mac.averageWaitTime*numPeople
                 create mac instance here
                 */
                    try {
                        String mac_OH = TabDemo.readOH("Macdonald");
                        String mac_bf_menu = TabDemo.readMenu("Macdonald-bf");
                        String mac_menu = TabDemo.readMenu("Macdonald-normal");
                        Macdonald mac = new Macdonald("Macdonald", mac_OH, mac_menu, 1, mac_bf_menu);
                        int mac_waitTime = mac.calculateWaitTime(numPeople);
                        JOptionPane.showMessageDialog(null, "Estimated waiting time : " + mac_waitTime + " min");
                    } catch (IOException ex) {
                        ex.printStackTrace();
                    }
                }
            });
            waitTimeBt_card1.setBounds(550, 10, 120, 30);
            card1.add(waitTimeBt_card1);

            JButton OHBt_card1 = new JButton("Operating Hour");
            OHBt_card1.addActionListener(new ActionListener() {
                @Override
                public void actionPerformed(ActionEvent e) {    // for pressing operating hour button
                    try {
                        String mac_OH = TabDemo.readOH("Macdonald").replace("null", "");
                        JOptionPane.showMessageDialog(null, mac_OH);
                    } catch (IOException ex) {
                        ex.printStackTrace();
                    }

                }
            });
            OHBt_card1.setBounds(550, 50, 120, 30);
            card1.add(OHBt_card1);
            tabbedPane.addTab(MACPANEL, card1);
        }



        // card2 - subway
        if(subway) {
            JPanel card2 = new JPanel() {
                public void paintComponent(Graphics g) {
                    // get the background image for subway menu card
                    ImageIcon img = new ImageIcon("src\\images\\subway.jpg");
                    System.out.println(g.drawImage(img.getImage(), 0, 0, 700, 500, null));
                    super.paintComponent(g);
                }
            };
            card2.setOpaque(false);
            card2.setLayout(null);
            String subwayMenu_new = subwayMenu.replace("null","");
            System.out.println(subwayMenu_new);
            JTextArea textArea = new JTextArea(3, 20);
            textArea.setText(subwayMenu_new);
            textArea.setWrapStyleWord(true);
            textArea.setLineWrap(true);
            textArea.setOpaque(false);
            textArea.setEditable(false);
            textArea.setFocusable(false);
            textArea.setForeground(Color.WHITE);
            textArea.setBackground(UIManager.getColor("Label.background"));
            textArea.setFont(new Font("Forte", Font.BOLD, 18));
            textArea.setBorder(UIManager.getBorder("Label.border"));
            textArea.setBounds(50,50,200,400);
            card2.add(textArea);

            // button field
            JButton waitTimeBt_card2 = new JButton("Wait Time");
            waitTimeBt_card2.addActionListener(new ActionListener() {
                @Override
                public void actionPerformed(ActionEvent e) {    // for pressing waitTime button
                    String numPeople = JOptionPane.showInputDialog(null, "please enter how many people in the queue:");
                    try {
                        String subway_OH = TabDemo.readOH("Subway");
                        String subway_menu = TabDemo.readMenu("Subway");
                        Subway subway = new Subway("Subway", subway_OH, subway_menu, 3);
                        int subway_waitTime = subway.calculateWaitTime(numPeople);
                        JOptionPane.showMessageDialog(null, "Estimated waiting time : " + subway_waitTime + " min");
                    } catch (IOException ex) {
                        ex.printStackTrace();
                    }
                }
            });
            waitTimeBt_card2.setBounds(550, 10, 120, 30);
            card2.add(waitTimeBt_card2);

            JButton OHBt_card2 = new JButton("Operating Hour");
            OHBt_card2.addActionListener(new ActionListener() {
                @Override
                public void actionPerformed(ActionEvent e) {    // for pressing operating hour button
                    Stall stall = new Stall();
                    try {
                        String Subway_OH = TabDemo.readOH("Subway").replace("null", "");
                        JOptionPane.showMessageDialog(null, Subway_OH);
                    } catch (IOException ex) {
                        ex.printStackTrace();
                    }

                }
            });
            OHBt_card2.setBounds(550, 50, 120, 30);
            card2.add(OHBt_card2);
            tabbedPane.addTab(SUBWAYPANEL, card2);
        }




        // card3 - western
        if(western) {
            JPanel card3 = new JPanel() {
                public void paintComponent(Graphics g) {
                    // get the background image for western menu page
                    ImageIcon img = new ImageIcon("src\\images\\western.jpg");
                    System.out.println(g.drawImage(img.getImage(), 0, 0, null));
                    super.paintComponent(g);
                }
            };
            card3.setOpaque(false);
            card3.setLayout(null);
            String westernMenu_new = westernMenu.replace("null","");
            System.out.println(westernMenu_new);
            JTextArea textArea = new JTextArea(3, 20);
            textArea.setText(westernMenu_new);
            textArea.setWrapStyleWord(true);
            textArea.setLineWrap(true);
            textArea.setOpaque(false);
            textArea.setEditable(false);
            textArea.setFocusable(false);
            textArea.setForeground(Color.WHITE);
            textArea.setBackground(UIManager.getColor("Label.background"));
            textArea.setFont(new Font("Forte", Font.BOLD, 18));
            textArea.setBorder(UIManager.getBorder("Label.border"));
            textArea.setBounds(450,50,200,400);
            card3.add(textArea);
            // button field
            JButton waitTimeBt_card3 = new JButton("Wait Time");
            waitTimeBt_card3.addActionListener(new ActionListener() {
                @Override
                public void actionPerformed(ActionEvent e) {    // for pressing waitTime button
                    String numPeople = JOptionPane.showInputDialog(null, "please enter how many people in the queue:");
                    try {
                        String western_OH = TabDemo.readOH("Western");
                        String western_bf_menu = TabDemo.readMenu("Western-bf");
                        String western_menu = TabDemo.readMenu("Western-normal");
                        Western western = new Western("Western", western_OH, western_menu, 3, western_bf_menu);
                        int western_waitTime = western.calculateWaitTime(numPeople);
                        JOptionPane.showMessageDialog(null, "Estimated waiting time : " + western_waitTime + " min");
                    } catch (IOException ex) {
                        ex.printStackTrace();
                    }
                }
            });
            waitTimeBt_card3.setBounds(30, 10, 120, 30);
            card3.add(waitTimeBt_card3);

            JButton OHBt_card3 = new JButton("Operating Hour");
            OHBt_card3.addActionListener(new ActionListener() {
                @Override
                public void actionPerformed(ActionEvent e) {    // for pressing operating hour button
                    Stall stall = new Stall();
                    try {
                        String Western_OH = TabDemo.readOH("Western").replace("null", "");
                        JOptionPane.showMessageDialog(null, Western_OH);
                    } catch (IOException ex) {
                        ex.printStackTrace();
                    }

                }
            });
            OHBt_card3.setBounds(30, 50, 120, 30);
            card3.add(OHBt_card3);
            tabbedPane.addTab(WESTERNPANEL,card3);
        }




        // card4 - malay food
        if(malay) {
            JPanel card4 = new JPanel() {
                public void paintComponent(Graphics g) {
                    // get background image for malay menu page
                    ImageIcon img = new ImageIcon("src\\images\\malay.jpg");
                    System.out.println(g.drawImage(img.getImage(), 0, 0, 700, 500, null));
                    super.paintComponent(g);
                }
            };
            card4.setOpaque(false);
            card4.setLayout(null);
            String malayMenu_new = malayMenu.replace("null","");
            System.out.println(malayMenu_new);
            JTextArea textArea = new JTextArea(3, 20);
            textArea.setText(malayMenu_new);
            textArea.setWrapStyleWord(true);
            textArea.setLineWrap(true);
            textArea.setOpaque(false);
            textArea.setEditable(false);
            textArea.setFocusable(false);
            textArea.setForeground(Color.WHITE);
            textArea.setBackground(UIManager.getColor("Label.background"));
            textArea.setFont(new Font("Forte", Font.BOLD, 18));
            textArea.setBorder(UIManager.getBorder("Label.border"));
            textArea.setBounds(500,50,200,400);
            card4.add(textArea);
            // button field
            JButton waitTimeBt_card4 = new JButton("Wait Time");
            waitTimeBt_card4.addActionListener(new ActionListener() {
                @Override
                public void actionPerformed(ActionEvent e) {    // for pressing waitTime button
                    String numPeople = JOptionPane.showInputDialog(null, "please enter how many people in the queue:");
                    try {
                        String malay_OH = TabDemo.readOH("Malay");
                        String malay_menu = TabDemo.readMenu("Malay-135");
                        String malay_alt_menu = TabDemo.readMenu("Malay-246");
                        Malay malay = new Malay("Malay,", malay_OH, malay_menu, 1, malay_alt_menu);
                        int malay_waitTime = malay.calculateWaitTime(numPeople);
                        JOptionPane.showMessageDialog(null, "Estimated waiting time : " + malay_waitTime + " min");
                    } catch (IOException ex) {
                        ex.printStackTrace();
                    }
                }
            });
            waitTimeBt_card4.setBounds(30, 10, 120, 30);
            card4.add(waitTimeBt_card4);

            JButton OHBt_card4 = new JButton("Operating Hour");
            OHBt_card4.addActionListener(new ActionListener() {
                @Override
                public void actionPerformed(ActionEvent e) {    // for pressing operating hour button
                    Stall stall = new Stall();
                    try {
                        String Malay_OH = TabDemo.readOH("Malay").replace("null", "");
                        JOptionPane.showMessageDialog(null, Malay_OH);
                    } catch (IOException ex) {
                        ex.printStackTrace();
                    }

                }
            });
            OHBt_card4.setBounds(30, 50, 120, 30);
            card4.add(OHBt_card4);
            tabbedPane.addTab(MALAYPANEL, card4);
        }




        // card5 - chicken rice
        if(chickenRice) {
            JPanel card5 = new JPanel() {
                public void paintComponent(Graphics g) {
                    // get the background image for chicken rice menu page
                    ImageIcon img = new ImageIcon("src\\images\\chicken rice.jpg");
                    System.out.println(g.drawImage(img.getImage(), 0, 0, 700, 500, null));
                    super.paintComponent(g);
                }
            };
            card5.setOpaque(false);
            card5.setLayout(null);
            String chickenRiceMenu_new = chickenRiceMenu.replace("null","");
            System.out.println(chickenRiceMenu_new);
            JTextArea textArea = new JTextArea(3, 20);
            textArea.setText(chickenRiceMenu_new);
            textArea.setWrapStyleWord(true);
            textArea.setLineWrap(true);
            textArea.setOpaque(false);
            textArea.setEditable(false);
            textArea.setFocusable(false);
            textArea.setBackground(UIManager.getColor("Label.background"));
            textArea.setFont(new Font("Forte", Font.BOLD, 18));
            textArea.setBorder(UIManager.getBorder("Label.border"));
            textArea.setBounds(50,50,200,400);
            card5.add(textArea);
            // button field
            JButton waitTimeBt_card5 = new JButton("Wait Time");
            waitTimeBt_card5.addActionListener(new ActionListener() {
                @Override
                public void actionPerformed(ActionEvent e) {    // for pressing waitTime button
                    String numPeople = JOptionPane.showInputDialog(null, "please enter how many people in the queue:");
                    try {
                        String chickenRice_OH = TabDemo.readOH("Chicken rice");
                        String chickenRice_menu = TabDemo.readMenu("Chicken rice");
                        ChickenRice chicken_rice = new ChickenRice("Chicken rice", chickenRice_OH, chickenRice_menu, 2);
                        int chickenRice_waitTime = chicken_rice.calculateWaitTime(numPeople);
                        JOptionPane.showMessageDialog(null, "Estimated waiting time : " + chickenRice_waitTime + " min");
                    } catch (IOException ex) {
                        ex.printStackTrace();
                    }
                }
            });
            waitTimeBt_card5.setBounds(550, 10, 120, 30);
            card5.add(waitTimeBt_card5);
            JButton OHBt_card5 = new JButton("Operating Hour");
            OHBt_card5.addActionListener(new ActionListener() {
                @Override
                public void actionPerformed(ActionEvent e) {    // for pressing operating hour button
                    Stall stall = new Stall();
                    try {
                        String ChickenRice_OH = TabDemo.readOH("Chicken rice").replace("null", "");
                        JOptionPane.showMessageDialog(null, ChickenRice_OH);
                    } catch (IOException ex) {
                        ex.printStackTrace();
                    }

                }
            });
            OHBt_card5.setBounds(550, 50, 120, 30);
            card5.add(OHBt_card5);
            tabbedPane.addTab(ChICKENRICEPANEL,card5);
        }

        pane.add(tabbedPane, BorderLayout.CENTER);
    }



    /**
     * Create the GUI and show it.  For thread safety,
     * this method should be invoked from the
     * event dispatch thread.
     */
    private static void createMainFrame() throws IOException {
        //Create and set up the window.
        JFrame mainFrame = new JFrame("Canteen Information System");
        mainFrame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        // here create the main menu panel
        mainFrame.setResizable(false);
        // set the background color to yellow
        Container mainPanel = mainFrame.getContentPane();
        mainPanel.setBackground(Color.BLACK);
        mainPanel.setPreferredSize(new Dimension(700, 500));

        // set this mainPanel layout as null (freestyle)
        mainPanel.setLayout(null);
        // create a image on it
        try {
            BufferedImage myImg = ImageIO.read(new File("C:\\Users\\DELL\\IdeaProjects\\Demo\\src\\images\\wall_paper.jpg"));
            // set the image size same with the label container
            Image myPicture = myImg.getScaledInstance(700, 450,
                    Image.SCALE_SMOOTH);
            JLabel picLabel = new JLabel(new ImageIcon(myPicture));
            picLabel.setBounds(0,50,700,450);
            mainPanel.add(picLabel);
        }
        catch (IOException ex){
            System.out.println("Can't open this image.");
        }

        // create title for the app
        JLabel appTitle = new JLabel("Canteen Inforation System");
        appTitle.setFont(new Font("Forte", Font.BOLD, 18));
        appTitle.setForeground(Color.YELLOW);
        appTitle.setBounds(10,5,250,40);
        mainPanel.add(appTitle);

        // create two Jbutton, one for View today, one for view other date
        JButton btViewToday = new JButton("View Today Stall");
        JButton btViewOtherDate = new JButton("View Other Date");
        btViewToday.setBounds(420,10,130,30);
        btViewOtherDate.setBounds(560,10,130,30);
        mainPanel.add(btViewToday);
        mainPanel.add(btViewOtherDate);
        // add actionListener for both btViewToday and btViewOtherDate
        btViewToday.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {    // for pressing view today's stall
                try {
                    createMenuFrame("today");
                } catch (IOException | ParseException ex) {
                    ex.printStackTrace();
                }
            }
        });

        btViewOtherDate.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {    // for pressing view other date
                try {
                    createMenuFrame("other date");
                } catch (IOException | ParseException ex) {
                    ex.printStackTrace();
                }
            }
        });




        // before entering the menu display page, you need a actionListener to trigger it
        // means you need to create another frame
        // Display the window.
        mainFrame.pack();
        mainFrame.setVisible(true);
    }

    public static void createMenuFrame(String mode) throws IOException, ParseException {
        if(mode.equals("today")){
            // get current date and time
            String timeStamp = new SimpleDateFormat("yyyy:MM:dd_HH:mm:ss").format(Calendar.getInstance().getTime());
            String time_str = timeStamp.split("_")[1];
            // get hour and minute
            int hour = Integer.parseInt(time_str.split(":")[0]);
            Date now = new Date();
            SimpleDateFormat simpleDateFormat= new SimpleDateFormat("EEEE");

            // get macdonald menu
            String mac_OH = TabDemo.readOH("Macdonald");
            String mac_bf_menu = TabDemo.readMenu("Macdonald-bf");
            String mac_menu = TabDemo.readMenu("Macdonald-normal");
            Macdonald mac = new Macdonald("Macdonald",mac_OH,mac_menu,1,mac_bf_menu);
            boolean isOpenMac = mac.isOpening(simpleDateFormat.format(now),hour);
            String mac_menu_display = "";
            if(isOpenMac){
                mac_menu_display = mac.get_correct_menu(hour);
            }

            // get subway menu
            String subway_OH = TabDemo.readOH("Subway");
            String subway_menu = TabDemo.readMenu("Subway");
            Subway subway = new Subway("Subway",subway_OH,subway_menu,3);
            boolean isOpenSubway = subway.isOpening(simpleDateFormat.format(now),hour);
            String subway_menu_display = "";
            if(isOpenSubway){
                subway_menu_display = subway.get_menu();
            }

            // get western menu
            String western_OH = TabDemo.readOH("Western");
            String western_bf_menu = TabDemo.readMenu("Western-bf");
            String western_menu = TabDemo.readMenu("Western");
            Western western = new Western("Western",western_OH,western_menu,3,western_bf_menu);
            boolean isOpenWestern = western.isOpening(simpleDateFormat.format(now),hour);
            String western_menu_display = "";
            if(isOpenWestern){
                western_menu_display = western.get_correct_menu(hour);
            }

            // get malay menu
            String malay_OH = TabDemo.readOH("Malay");
            String malay_menu = TabDemo.readMenu("Malay-135");
            String malay_alt_menu = TabDemo.readMenu("Malay-246");
            Malay malay = new Malay("Malay,",malay_OH,malay_menu,1,malay_alt_menu);
            boolean isOpenMalay = malay.isOpening(simpleDateFormat.format(now),hour);
            String malay_menu_display = "";
            if(isOpenMalay){
                malay_menu_display = malay.get_correct_menu(simpleDateFormat.format(now));
            }

            // get chicken rice menu
            String chickenRice_OH = TabDemo.readOH("Chicken rice");
            String chickenRice_menu = TabDemo.readMenu("Chicken rice");
            ChickenRice chicken_rice = new ChickenRice("Chicken rice",chickenRice_OH,chickenRice_menu,2);
            boolean isOpenChickenRice = chicken_rice.isOpening(simpleDateFormat.format(now),hour);
            String chickenRice_menu_display = "";
            if(isOpenChickenRice){
                chickenRice_menu_display = chicken_rice.get_menu();
            }

            // menu page title
            JFrame menuFrame = new JFrame("Opening Stalls");
            TabDemo demo = new TabDemo();
            Container menuPane = menuFrame.getContentPane();
            demo.addComponentToPane(menuPane,isOpenMac,isOpenSubway,isOpenWestern,isOpenMalay,isOpenChickenRice,
                    mac_menu_display,subway_menu_display,western_menu_display,malay_menu_display,chickenRice_menu_display);
            menuFrame.pack();
            menuFrame.setVisible(true);
        }
        // if user press view stall by other date
        else{
            // create message box ask for date and time
            String inputDate = JOptionPane.showInputDialog(null, "Enter time(yyyy-mm-dd)");
            try {
                Date date = new SimpleDateFormat("yyyy-M-d").parse(inputDate);
                // Then get the day of week from the Date based on specific locale.
                String dayOfWeek = new SimpleDateFormat("EEEE", Locale.ENGLISH).format(date);
                System.out.println(dayOfWeek);

                String inputTime = JOptionPane.showInputDialog(null, "Enter time(hh:mm)");

                int input_hour = Integer.parseInt(inputTime.split(":")[0]);

                String mac_OH = TabDemo.readOH("Macdonald");
                String mac_bf_menu = TabDemo.readMenu("Macdonald-bf");
                String mac_menu = TabDemo.readMenu("Macdonald-normal");
                Macdonald mac = new Macdonald("Macdonald", mac_OH, mac_menu, 1, mac_bf_menu);
                boolean isOpenMac = mac.isOpening(dayOfWeek, input_hour);
                String mac_menu_display = "";
                if (isOpenMac) {
                    mac_menu_display = mac.get_correct_menu(input_hour);
                }


                String subway_OH = TabDemo.readOH("Subway");
                String subway_menu = TabDemo.readMenu("Subway");
                Subway subway = new Subway("Subway", subway_OH, subway_menu, 3);
                boolean isOpenSubway = subway.isOpening(dayOfWeek, input_hour);
                String subway_menu_display = "";
                if (isOpenSubway) {
                    subway_menu_display = subway.get_menu();
                }


                String western_OH = TabDemo.readOH("Western");
                String western_bf_menu = TabDemo.readMenu("Western-bf");
                String western_menu = TabDemo.readMenu("Western");
                Western western = new Western("Western", western_OH, western_menu, 3, western_bf_menu);
                boolean isOpenWestern = western.isOpening(dayOfWeek, input_hour);
                String western_menu_display = "";
                if (isOpenWestern) {
                    western_menu_display = western.get_correct_menu(input_hour);
                }


                String malay_OH = TabDemo.readOH("Malay");
                String malay_menu = TabDemo.readMenu("Malay-135");
                String malay_alt_menu = TabDemo.readMenu("Malay-246");
                Malay malay = new Malay("Malay,", malay_OH, malay_menu, 1, malay_alt_menu);
                boolean isOpenMalay = malay.isOpening(dayOfWeek, input_hour);
                String malay_menu_display = "";
                if (isOpenMalay) {
                    malay_menu_display = malay.get_correct_menu(dayOfWeek);
                }


                String chickenRice_OH = TabDemo.readOH("Chicken rice");
                String chickenRice_menu = TabDemo.readMenu("Chicken rice");
                ChickenRice chicken_rice = new ChickenRice("Chicken rice", chickenRice_OH, chickenRice_menu, 2);
                boolean isOpenChickenRice = chicken_rice.isOpening(dayOfWeek, input_hour);
                String chickenRice_menu_display = "";
                if (isOpenChickenRice) {
                    chickenRice_menu_display = chicken_rice.get_menu();
                }


                JFrame menuFrame = new JFrame("Opening Stalls");
                TabDemo demo = new TabDemo();
                Container menuPane = menuFrame.getContentPane();
                demo.addComponentToPane(menuPane,isOpenMac,isOpenSubway,isOpenWestern,isOpenMalay,isOpenChickenRice,
                        mac_menu_display,subway_menu_display,western_menu_display,malay_menu_display,chickenRice_menu_display);
                menuFrame.pack();
                menuFrame.setVisible(true);
            }
            catch (Exception e){
                    System.out.println("Invalid input.");
            }
        }
    }

    public static void main(String[] args) throws IOException {
        /* Use an appropriate Look and Feel */
        try {
            UIManager.setLookAndFeel("javax.swing.plaf.metal.MetalLookAndFeel");
        } catch (UnsupportedLookAndFeelException ex) {
            ex.printStackTrace();
        } catch (IllegalAccessException ex) {
            ex.printStackTrace();
        } catch (InstantiationException ex) {
            ex.printStackTrace();
        } catch (ClassNotFoundException ex) {
            ex.printStackTrace();
        }
        /* Turn off metal's use of bold fonts */
        UIManager.put("swing.boldMetal", Boolean.FALSE);


        //Schedule a job for the event dispatch thread:
        //creating and showing this application's GUI.
        javax.swing.SwingUtilities.invokeLater(new Runnable() {
            public void run() {
                try {
                    createMainFrame();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        });
    }


    public static void readToBuffer(StringBuffer buffer, String filePath) throws IOException {
        InputStream is = new FileInputStream(filePath);
        String line;    // use for save content in each line
        BufferedReader reader = new BufferedReader(new InputStreamReader(is));
        line = reader.readLine();   // read the first line
        while (line != null) {  // if line read is null, means EOF
            buffer.append(line);    // add the line content into the buffer
            buffer.append("\n");    // add new line character after each line content
            line = reader.readLine();   // read the next line
        }
        reader.close();
        is.close();
    }

    // read menu (call readToBuffer method)
    public static String readMenu(String stall_name) throws IOException {
        StringBuffer buffer = new StringBuffer();
        TabDemo.readToBuffer(buffer,"src/all_menu.txt");
        String all_menu = buffer.toString();
        String[] all_menu_array = all_menu.split("--------------------");
        String foundMenu = null;
        for(int i=0;i<all_menu_array.length;i++){
            if(all_menu_array[i].indexOf(stall_name) != -1){
                foundMenu += all_menu_array[i];
            }
        }
        return foundMenu;
    }

    // read operating hours (call readToBuffer method)
    public static String readOH(String stall_name) throws IOException {
        StringBuffer buffer = new StringBuffer();
        TabDemo.readToBuffer(buffer,"src/all_OH.txt");
        String all_OH = buffer.toString();
        String[] all_OH_array = all_OH.split("--------------------");
        String foundOH = null;
        for(int i=0;i<all_OH_array.length;i++){
            if(all_OH_array[i].indexOf(stall_name) != -1){
                foundOH += all_OH_array[i];
            }
        }
        return foundOH;
    }

}