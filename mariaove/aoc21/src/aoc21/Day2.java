package aoc21;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Scanner;

public class Day2 {
	
	
	public static ArrayList<String> datos = new ArrayList<String>(); // Create an ArrayList object
	public static void main(String[] args) throws FileNotFoundException {
		// TODO Auto-generated method stub

		 File doc = new File("C:\\Users\\ovejerom\\eclipse-workspace\\aoc21\\src\\aoc21\\data\\reto2.txt");
	
		
		        Scanner obj = new Scanner(doc);

		        while (obj.hasNextLine()) {
		        	datos.add(obj.nextLine());
		        }
	}
	
	
	public static void parte1() {
		int x=0;
		int y =0;
		for (int i = 0; i <datos.size();i++) {
			String aux = (String) datos.get(i);
			String[] parts = aux.split(" ");
			switch(parts[0]) {
			case "forward":
				x= x+ Integer.parseInt(parts[1]);
				break;
			case "up":
				y= y- Integer.parseInt(parts[1]);
				break;
			case "down":
				y= y+ Integer.parseInt(parts[1]);
				break;
			}
		}
		System.out.println(x*y);
	}
	
	
	public static void parte2() {
		
		int x=0;
		int y =0;
		int aim = 0;
		
		for (int i = 0; i <datos.size();i++) {
			String aux = (String) datos.get(i);
			String[] parts = aux.split(" ");
			switch(parts[0]) {
			case "forward":
				x= x+ Integer.parseInt(parts[1]);
				y = y + (Integer.parseInt(parts[1])*aim);
				break;
			case "up":
				aim = aim - Integer.parseInt(parts[1]);
				break;
			case "down":
				aim = aim + Integer.parseInt(parts[1]);
				break;
			}
		}
		System.out.println(x*y);
	}
}
