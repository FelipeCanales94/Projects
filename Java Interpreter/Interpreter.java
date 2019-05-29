import java.io.*;
import java.util.*;

public class interpreter {

    public static String error = ":error:";
    public static int positive = 0;
    public static ArrayList<String> stackArray = new ArrayList<>();
    //push function taking in a string and stack. Will be using multiple stacks so this function
    // is neccesary to avoid confusion
    public static void push(String input, Stack stack) {
        stack.push(input);
    }

    //check if a string contains a number
    public static boolean checkForNumber(String string) {
        char array[] = string.toCharArray();
        for (int i = 0; i < string.length(); i++) {
            if (!Character.isLetter(array[i])) {
                return true;
            }
        }

        return false;
    }


    //check if something is :true: or :false: in stack
    public static boolean checkBoolean(String string) {
        if (string.equals(":true:")) {
            return true;
        }

        return false;
    }

    //check if top of stack is a number or valid string without quotes
    public static boolean validTop(Stack stack) {
        //char quotes = stack.peek().toString().charAt(0);

        if (stack.peek().toString().equals(":true:") || stack.peek().toString().equals(":false:") || stack.peek().toString().equals(":unit:") || stack.peek().toString().equals(":error:")) {
            return false;
        }

        return true;
    }

    public static int letFunction(Stack stack, HashMap<String, String> hash, ArrayList<String> stackArray, int letCounter) {
        Stack letStack = new Stack();
        // letStack = (Stack<String>) stack.clone();
        HashMap<String, String> letHash = new HashMap<>();
        letHash.putAll(hash);
        letCounter = letCounter + 1;

        String lineRead = stackArray.get(letCounter);

        while (!lineRead.equals("end")) {
            lineRead = stackArray.get(letCounter);
            letCounter = checkFunction(lineRead, letStack, letHash, stackArray, letCounter);

            if (lineRead.equals("end")) {
                if (letStack.isEmpty()) {
                } else {
                    stack.push(letStack.pop());
                    return letCounter;
                }
            }
            letCounter = letCounter + 1;
        }
        return letCounter;
    }


    public static int checkFunction(String lineRead, Stack stack, HashMap<String, String> hash, ArrayList<String> stackArray, int letCounter) {
        String hold = "";
        String hold2 = "";
        String hold3 = "";
        int parsed = 0;
        int parsed2 = 0;


        if (lineRead.equals("let")) {
            letCounter = letFunction(stack, hash, stackArray, letCounter);
            return letCounter;
        }


        /****************************************** Pop ******************************************/
        if (lineRead.equals("pop")) {
            if (stack.isEmpty()) {
                push(error, stack);
            } else {
                stack.pop();
            }
            return letCounter;
        }


        /****************************************** Swap ******************************************/
        if (lineRead.equals("swap")) {
            String tempHold = "";
            String tempHold2 = "";
            if (stack.size() < 2) {
                push(error, stack);
            } else {

                hold = stack.pop().toString();
                hold2 = stack.pop().toString();
                stack.push(hold);
                stack.push(hold2);

            }
        }


        /****************************************** Negative ******************************************/
        if (lineRead.equals("neg")) {

            String tempHold = "";
            String tempHold2 = "";
            if (stack.isEmpty()) {      //if stack empty, push :error:
                push(error, stack);
            } else {
                if (validTop(stack)) { //if top of stack is anything but a number, throw error, else check hashmap
                    hold = stack.pop().toString();
                    tempHold = hold;

                    if ((Character.isDigit(hold.charAt(0)) == false && hold.charAt(0) != '-') && hash.containsKey(hold) == false) {
                        push(tempHold, stack);
                        push(error, stack);
                    } else {
                        if (hash.containsKey(hold)) {
                            if (Character.isDigit(hash.get(hold).charAt(0)) == false && hash.get(hold).charAt(0) != '-') {
                                push(tempHold, stack);
                                push(error, stack);
                                return letCounter;
                            } else {
                                hold = hash.get(hold);
                            }
                        }
                        if (hold.charAt(0) == '-') {
                            parsed = Integer.parseInt(hold.substring(1, hold.length()));
                        } else {
                            parsed = Integer.parseInt(hold) * -1;
                        }
                        push(Integer.toString(parsed), stack);

                    }
                } else {
                    push(error, stack);
                }
            }
        }

        /****************************************** Remainder ******************************************/
        if (lineRead.equals("rem")) {
            String tempHold = "";
            String tempHold2 = "";
            if (stack.isEmpty()) {      //if stack empty, push :error:
                push(error, stack);
            } else {
                if (validTop(stack)) { //if top of stack is anything but a number, throw error, else check hashmap
                    hold = stack.pop().toString();
                    tempHold = hold;

                    if ((Character.isDigit(hold.charAt(0)) == false && hold.charAt(0)!='-') && hash.containsKey(hold) == false) {
                        push(tempHold, stack);
                        push(error, stack);
                    } else {
                        if (hash.containsKey(hold)) {
                            if (Character.isDigit(hash.get(hold).charAt(0)) == false && hash.get(hold).charAt(0)!='-') {
                                push(tempHold, stack);
                                push(error, stack);
                                return letCounter;
                            } else {
                                hold = hash.get(hold);
                            }
                        }
                        if (hold.charAt(0) == '-') {  //if negative, parse then multiply by -1
                            parsed = Integer.parseInt(hold.substring(1, hold.length())) * -1;
                        } else {
                            parsed = Integer.parseInt(hold);
                        }
                        if (stack.isEmpty()) { // check if stack is empty after getting first number
                            push(tempHold, stack);
                            push(error, stack);
                        } else {
                            if (validTop(stack)) { //check if second number is an actual number
                                hold2 = stack.pop().toString();
                                tempHold2 = hold2;
                                //      System.out.println(hash.get(hold2));

                                if ((Character.isDigit(hold2.charAt(0)) == false && hold2.charAt(0)!='-') && hash.containsKey(hold2) == false) {
                                    push(tempHold2, stack);
                                    push(tempHold, stack);
                                    push(error, stack);
                                } else {
                                    if (hash.containsKey(hold2)) { //check if it's in hashmap
                                        if (Character.isDigit(hash.get(hold2).charAt(0)) == false && hash.get(hold2).charAt(0)!='-') {
                                            push(tempHold2, stack);
                                            push(tempHold, stack);
                                            push(error, stack);
                                            return letCounter;
                                        } else {
                                            hold2 = hash.get(hold2);
                                        }
                                    }
                                    if (hold.equals("0")) {
                                        push(tempHold2, stack);
                                        push(tempHold, stack);
                                        push(error, stack);
                                        return letCounter;
                                    } else {
                                        if (hold2.charAt(0) == '-') { //if negative mult by -1
                                            parsed2 = Integer.parseInt(hold2.substring(1)) * -1;
                                        } else {
                                            parsed2 = Integer.parseInt(hold2);
                                        }
                                    }
                                    int remainder = parsed2 % parsed;
                                    push(Integer.toString(remainder), stack); //add the 2 and push to stack

                                }
                            } else { //if second number is not valid, error
                                push(tempHold, stack);
                                push(error, stack);
                            }
                        }
                    }
                } else { //if first number is not valid, error
                    push(error, stack);
                }

            }
        }

        /****************************************** div ******************************************/

        if (lineRead.equals("div")) {

            String tempHold = "";
            String tempHold2 = "";
            if (stack.isEmpty()) {      //if stack empty, push :error:
                push(error, stack);
            } else {
                if (validTop(stack)) { //if top of stack is anything but a number, throw error, else check hashmap
                    hold = stack.pop().toString();
                    tempHold = hold;

                    if ((Character.isDigit(hold.charAt(0)) == false && hold.charAt(0)!='-') && hash.containsKey(hold) == false) {
                        push(tempHold, stack);
                        push(error, stack);
                    } else {
                        if (hash.containsKey(hold)) {
                            if (Character.isDigit(hash.get(hold).charAt(0)) == false && hash.get(hold).charAt(0)!='-') {
                                push(tempHold, stack);
                                push(error, stack);
                                return letCounter;
                            } else {
                                hold = hash.get(hold);
                            }
                        }
                        if (hold.charAt(0) == '-') {  //if negative, parse then multiply by -1
                            parsed = Integer.parseInt(hold.substring(1, hold.length())) * -1;
                        } else {
                            parsed = Integer.parseInt(hold);
                        }
                        if (stack.isEmpty()) { // check if stack is empty after getting first number
                            push(tempHold, stack);
                            push(error, stack);
                        } else {
                            if (validTop(stack)) { //check if second number is an actual number
                                hold2 = stack.pop().toString();
                                tempHold2 = hold2;
                                //      System.out.println(hash.get(hold2));

                                if ((Character.isDigit(hold2.charAt(0)) == false && hold2.charAt(0)!='-') && hash.containsKey(hold2) == false) {
                                    push(tempHold2, stack);
                                    push(tempHold, stack);
                                    push(error, stack);
                                } else {
                                    if (hash.containsKey(hold2)) { //check if it's in hashmap
                                        if (Character.isDigit(hash.get(hold2).charAt(0)) == false && hash.get(hold2).charAt(0)!='-') {
                                            push(tempHold2, stack);
                                            push(tempHold, stack);
                                            push(error, stack);
                                            return letCounter;
                                        } else {
                                            hold2 = hash.get(hold2);
                                        }
                                    }
                                    if (hold.equals("0")) {
                                        push(tempHold2, stack);
                                        push(tempHold, stack);
                                        push(error, stack);
                                        return letCounter;
                                    } else {
                                        if (hold2.charAt(0) == '-') { //if negative mult by -1
                                            parsed2 = Integer.parseInt(hold2.substring(1)) * -1;
                                        } else {
                                            parsed2 = Integer.parseInt(hold2);
                                        }
                                    }
                                    int quotient = parsed2 / parsed;
                                    push(Integer.toString(quotient), stack); //add the 2 and push to stack

                                }
                            } else { //if second number is not valid, error
                                push(tempHold, stack);
                                push(error, stack);
                            }
                        }
                    }
                } else { //if first number is not valid, error
                    push(error, stack);
                }

            }
        }

        /****************************************** Mult ******************************************/

        if (lineRead.equals("mul")) {
            String tempHold = "";
            String tempHold2 = "";
            if (stack.isEmpty()) {      //if stack empty, push :error:
                push(error, stack);
            } else {
                if (validTop(stack)) { //if top of stack is anything but a number, throw error, else check hashmap
                    hold = stack.pop().toString();
                    tempHold = hold;

                    if ((Character.isDigit(hold.charAt(0)) == false && hold.charAt(0)!='-') && hash.containsKey(hold) == false) {
                        push(tempHold, stack);
                        push(error, stack);
                    } else {
                        if (hash.containsKey(hold)) {
                            if (Character.isDigit(hash.get(hold).charAt(0)) == false && hash.get(hold).charAt(0)!='-') {
                                push(tempHold, stack);
                                push(error, stack);
                                return letCounter;
                            } else {
                                hold = hash.get(hold);
                            }
                        }
                        if (hold.charAt(0) == '-') {  //if negative, parse then multiply by -1
                            parsed = Integer.parseInt(hold.substring(1, hold.length())) * -1;
                        } else {
                            parsed = Integer.parseInt(hold);
                        }
                        if (stack.isEmpty()) { // check if stack is empty after getting first number
                            push(tempHold, stack);
                            push(error, stack);
                        } else {
                            if (validTop(stack)) { //check if second number is an actual number
                                hold2 = stack.pop().toString();
                                tempHold2 = hold2;
                                //      System.out.println(hash.get(hold2));

                                if ((Character.isDigit(hold2.charAt(0)) == false && hold2.charAt(0)!='-') && hash.containsKey(hold2) == false) {
                                    push(tempHold2, stack);
                                    push(tempHold, stack);
                                    push(error, stack);
                                } else {
                                    if (hash.containsKey(hold2)) { //check if it's in hashmap
                                        if (Character.isDigit(hash.get(hold2).charAt(0)) == false && hash.get(hold2).charAt(0)!='-') {
                                            push(tempHold2, stack);
                                            push(tempHold, stack);
                                            push(error, stack);
                                            return letCounter;
                                        } else {
                                            hold2 = hash.get(hold2);
                                        }
                                    }
                                    if (hold2.charAt(0) == '-') { //if negative mult by -1
                                        parsed2 = Integer.parseInt(hold2.substring(1)) * -1;
                                    } else {
                                        parsed2 = Integer.parseInt(hold2);
                                    }
                                    int product = parsed2 * parsed;
                                    push(Integer.toString(product), stack); //add the 2 and push to stack

                                }
                            } else { //if second number is not valid, error
                                push(tempHold, stack);
                                push(error, stack);
                            }
                        }
                    }
                } else { //if first number is not valid, error
                    push(error, stack);
                }

            }

        }

        /****************************************** Sub ******************************************/
        if (lineRead.equals("sub")) {
            String tempHold = "";
            String tempHold2 = "";
            if (stack.isEmpty()) {      //if stack empty, push :error:
                push(error, stack);
            } else {
                if (validTop(stack)) { //if top of stack is anything but a number, throw error, else check hashmap
                    hold = stack.pop().toString();
                    tempHold = hold;

                    if ((Character.isDigit(hold.charAt(0)) == false && hold.charAt(0)!='-') && hash.containsKey(hold) == false) {
                        push(tempHold, stack);
                        push(error, stack);
                    } else {
                        if (hash.containsKey(hold)) {
                            if (Character.isDigit(hash.get(hold).charAt(0)) == false && hash.get(hold).charAt(0)!='-') {
                                push(tempHold, stack);
                                push(error, stack);
                                return letCounter;
                            } else {
                                hold = hash.get(hold);
                            }
                        }
                        if (hold.charAt(0) == '-') {  //if negative, parse then multiply by -1
                            parsed = Integer.parseInt(hold.substring(1, hold.length())) * -1;
                        } else {
                            parsed = Integer.parseInt(hold);
                        }
                        if (stack.isEmpty()) { // check if stack is empty after getting first number
                            push(tempHold, stack);
                            push(error, stack);
                        } else {
                            if (validTop(stack)) { //check if second number is an actual number
                                hold2 = stack.pop().toString();
                                tempHold2 = hold2;
                                //      System.out.println(hash.get(hold2));

                                if ((Character.isDigit(hold2.charAt(0)) == false && hold2.charAt(0)!='-') && hash.containsKey(hold2) == false) {
                                    push(tempHold2, stack);
                                    push(tempHold, stack);
                                    push(error, stack);
                                } else {
                                    if (hash.containsKey(hold2)) { //check if it's in hashmap
                                        if (Character.isDigit(hash.get(hold2).charAt(0)) == false && hash.get(hold2).charAt(0)!='-') {
                                            push(tempHold2, stack);
                                            push(tempHold, stack);
                                            push(error, stack);
                                            return letCounter;
                                        } else {
                                            hold2 = hash.get(hold2);
                                        }
                                    }
                                    if (hold2.charAt(0) == '-') { //if negative mult by -1
                                        parsed2 = Integer.parseInt(hold2.substring(1)) * -1;
                                    } else {
                                        parsed2 = Integer.parseInt(hold2);
                                    }
                                    int diff = parsed2 - parsed;
                                    push(Integer.toString(diff), stack); //add the 2 and push to stack

                                }
                            } else { //if second number is not valid, error
                                push(tempHold, stack);
                                push(error, stack);
                            }
                        }
                    }
                } else { //if first number is not valid, error
                    push(error, stack);
                }

            }
        }

        /****************************************** ADD ******************************************/

        if (lineRead.equals("add")) {
            String tempHold = "";
            String tempHold2 = "";
            if (stack.isEmpty()) {      //if stack empty, push :error:
                push(error, stack);
            } else {
                if (validTop(stack)) { //if top of stack is anything but a number, throw error, else check hashmap
                    hold = stack.pop().toString();
                    tempHold = hold;

                    if ((Character.isDigit(hold.charAt(0)) == false && hold.charAt(0)!='-') && hash.containsKey(hold) == false) {
                        push(tempHold, stack);
                        push(error, stack);
                    } else {
                        if (hash.containsKey(hold)) {
                            if (Character.isDigit(hash.get(hold).charAt(0)) == false && hash.get(hold).charAt(0)!='-') {
                                push(tempHold, stack);
                                push(error, stack);
                                return letCounter;
                            } else {
                                hold = hash.get(hold);
                            }
                        }
                        if (hold.charAt(0) == '-') {  //if negative, parse then multiply by -1
                            parsed = Integer.parseInt(hold.substring(1, hold.length())) * -1;
                        } else {
                            parsed = Integer.parseInt(hold);
                        }
                        if (stack.isEmpty()) { // check if stack is empty after getting first number
                            push(tempHold, stack);
                            push(error, stack);
                        } else {
                            if (validTop(stack)) { //check if second number is an actual number
                                hold2 = stack.pop().toString();
                                tempHold2 = hold2;
                                //      System.out.println(hash.get(hold2));

                                if ((Character.isDigit(hold2.charAt(0)) == false && hold2.charAt(0)!='-') && hash.containsKey(hold2) == false) {
                                    push(tempHold2, stack);
                                    push(tempHold, stack);
                                    push(error, stack);
                                } else {
                                    if (hash.containsKey(hold2)) { //check if it's in hashmap
                                        if (Character.isDigit(hash.get(hold2).charAt(0)) == false && hash.get(hold2).charAt(0)!='-') {
                                            push(tempHold2, stack);
                                            push(tempHold, stack);
                                            push(error, stack);
                                            return letCounter;
                                        } else {
                                            hold2 = hash.get(hold2);
                                        }
                                    }
                                    if (hold2.charAt(0) == '-') { //if negative mult by -1
                                        parsed2 = Integer.parseInt(hold2.substring(1)) * -1;
                                    } else {
                                        parsed2 = Integer.parseInt(hold2);
                                    }
                                    int sum = parsed + parsed2;
                                    push(Integer.toString(sum), stack); //add the 2 and push to stack

                                }
                            } else { //if second number is not valid, error
                                push(tempHold, stack);
                                push(error, stack);
                            }
                        }
                    }
                } else { //if first number is not valid, error
                    push(error, stack);
                }

            }
        }

        /****************************************** And ******************************************/
        if (lineRead.equals("and")) {
            String tempHold = "";
            String tempHold2 = "";
            if (stack.isEmpty()) {      //if stack empty, push :error:
                push(error, stack);
            } else {
                if ((stack.peek().toString().equals(":false:") || stack.peek().toString().equals(":true:")) || (hash.containsKey(stack.peek().toString()) && hash.get(stack.peek().toString()).equals(":true:")) || (hash.containsKey(stack.peek().toString()) && hash.get(stack.peek().toString()).equals(":false:"))) { //if top of stack is anything but a number, throw error, else check hashmap
                    hold = stack.pop().toString();
                    tempHold = hold;
                    if (hash.containsKey(hold)) {
                        hold = hash.get(hold);

                    }

                    if (stack.isEmpty()) { // check if stack is empty after getting first number
                        push(tempHold, stack);
                        push(error, stack);
                    } else {
                        if ((stack.peek().toString().equals(":false:") || stack.peek().toString().equals(":true:")) || (hash.containsKey(stack.peek().toString()) && hash.get(stack.peek().toString()).equals(":true:")) || (hash.containsKey(stack.peek().toString()) && hash.get(stack.peek().toString()).equals(":false:"))) { //if top of stack is anything but a number, throw error, else check hashmap
                            hold2 = stack.pop().toString();
                            if (hash.containsKey(hold2)) { //check if it's in hashmap
                                hold2 = hash.get(hold2);
                            }

                            Boolean input1 = checkBoolean(hold);
                            Boolean input2 = checkBoolean(hold2);
                            Boolean bool = (input1 & input2);
                            push(":" + bool.toString() + ":", stack);

                        } else { //if second input is not valid, error
                            push(tempHold, stack);
                            push(error, stack);
                        }
                    }
                } else { //if first input is not valid, error
                    push(error, stack);
                }

            }
        }


        /****************************************** Or ******************************************/
        if (lineRead.equals("or")) {

            String tempHold = "";
            String tempHold2 = "";
            if (stack.isEmpty()) {      //if stack empty, push :error:
                push(error, stack);
            } else {
                if ((stack.peek().toString().equals(":false:") || stack.peek().toString().equals(":true:")) || (hash.containsKey(stack.peek().toString()) && hash.get(stack.peek().toString()).equals(":true:")) || (hash.containsKey(stack.peek().toString()) && hash.get(stack.peek().toString()).equals(":false:"))) { //if top of stack is anything but a number, throw error, else check hashmap
                    hold = stack.pop().toString();
                    tempHold = hold;
                    if (hash.containsKey(hold)) {
                        hold = hash.get(hold);

                    }

                    if (stack.isEmpty()) { // check if stack is empty after getting first number
                        push(tempHold, stack);
                        push(error, stack);
                    } else {
                        if ((stack.peek().toString().equals(":false:") || stack.peek().toString().equals(":true:")) || (hash.containsKey(stack.peek().toString()) && hash.get(stack.peek().toString()).equals(":true:")) || (hash.containsKey(stack.peek().toString()) && hash.get(stack.peek().toString()).equals(":false:"))) { //if top of stack is anything but a number, throw error, else check hashmap
                            hold2 = stack.pop().toString();
                            if (hash.containsKey(hold2)) { //check if it's in hashmap
                                hold2 = hash.get(hold2);
                            }

                            Boolean input1 = checkBoolean(hold);
                            Boolean input2 = checkBoolean(hold2);
                            Boolean bool = (input1 | input2);
                            push(":" + bool.toString() + ":", stack);

                        } else { //if second input is not valid, error
                            push(tempHold, stack);
                            push(error, stack);
                        }
                    }
                } else { //if first input is not valid, error
                    push(error, stack);
                }

            }
        }

        /****************************************** Not ******************************************/
        if (lineRead.equals("not")) {
            String tempHold = "";
            String tempHold2 = "";
            if (stack.isEmpty()) {      //if stack empty, push :error:
                push(error, stack);
            } else {
                if (stack.peek().toString().equals(":false:") || stack.peek().toString().equals(":true:") || (!hash.isEmpty() && (hash.containsKey (stack.peek().toString()) && (hash.get(stack.peek().toString()).equals(":true:") || hash.get(stack.peek().toString()).equals(":false:"))))) { //if top of stack is anything but a number, throw error, else check hashmap
                    //if top of stack is anything but a number, throw error, else check hashmap
                    hold = stack.pop().toString();
                    tempHold = hold;
                    if (hash.containsKey(hold)) {
                        hold = hash.get(hold);
                    }
                    Boolean input1 = checkBoolean(hold);
                    Boolean bool = (!input1); //this line is useless but oh well lol
                    push(":" + bool.toString() + ":", stack);

                } else { //if second input is not valid, error
                    hold = stack.pop().toString();
                    push(hold, stack);
                    push(error, stack);

                }
            }
        }

        /****************************************** Equal ******************************************/
        if (lineRead.equals("equal")) {
            String tempHold = "";
            String tempHold2 = "";
            if (stack.isEmpty()) {      //if stack empty, push :error:
                push(error, stack);
            } else {
                if (validTop(stack)) { //if top of stack is anything but a number, throw error, else check hashmap
                    hold = stack.pop().toString();
                    tempHold = hold;

                    if ((Character.isDigit(hold.charAt(0)) == false && hold.charAt(0)!='-') && hash.containsKey(hold) == false) {
                        push(tempHold, stack);
                        push(error, stack);
                    } else {
                        if (hash.containsKey(hold)) {
                            if (Character.isDigit(hash.get(hold).charAt(0)) == false) {
                                push(tempHold, stack);
                                push(error, stack);
                                return letCounter;
                            } else {
                                hold = hash.get(hold);
                            }
                        }
                        if (hold.charAt(0) == '-') {  //if negative, parse then multiply by -1
                            parsed = Integer.parseInt(hold.substring(1, hold.length())) * -1;
                        } else {
                            parsed = Integer.parseInt(hold);
                        }
                        if (stack.isEmpty()) { // check if stack is empty after getting first number
                            push(tempHold, stack);
                            push(error, stack);
                        } else {
                            if (validTop(stack)) { //check if second number is an actual number
                                hold2 = stack.pop().toString();
                                tempHold2 = hold2;
                                //      System.out.println(hash.get(hold2));

                                if ((Character.isDigit(hold2.charAt(0)) == false && hold2.charAt(0)!='-') && hash.containsKey(hold2) == false) {
                                    push(tempHold2, stack);
                                    push(tempHold, stack);
                                    push(error, stack);
                                } else {
                                    if (hash.containsKey(hold2)) { //check if it's in hashmap
                                        if (Character.isDigit(hash.get(hold2).charAt(0)) == false) {
                                            push(tempHold2, stack);
                                            push(tempHold, stack);
                                            push(error, stack);
                                            return letCounter;
                                        } else {
                                            hold2 = hash.get(hold2);
                                        }
                                    }
                                    if (hold2.charAt(0) == '-') { //if negative mult by -1
                                        parsed2 = Integer.parseInt(hold2.substring(1)) * -1;
                                    } else {
                                        parsed2 = Integer.parseInt(hold2);
                                    }
                                    if(parsed == parsed2){
                                        push(":true:", stack);
                                    } else {
                                        push(":false:", stack);
                                    }
                                }
                            } else { //if second number is not valid, error
                                push(tempHold, stack);
                                push(error, stack);
                            }
                        }
                    }
                } else { //if first number is not valid, error
                    push(error, stack);
                }

            }
        }

        /****************************************** Less Than ******************************************/
        if (lineRead.equals("lessThan")) {
            String tempHold = "";
            String tempHold2 = "";
            if (stack.isEmpty()) {      //if stack empty, push :error:
                push(error, stack);
            } else {
                if (validTop(stack)) { //if top of stack is anything but a number, throw error, else check hashmap
                    hold = stack.pop().toString();
                    tempHold = hold;

                    if ((Character.isDigit(hold.charAt(0)) == false && hold.charAt(0)!='-') && hash.containsKey(hold) == false) {
                        push(tempHold, stack);
                        push(error, stack);
                    } else {
                        if (hash.containsKey(hold)) {
                            if (Character.isDigit(hash.get(hold).charAt(0)) == false) {
                                push(tempHold, stack);
                                push(error, stack);
                                return letCounter;
                            } else {
                                hold = hash.get(hold);
                            }
                        }
                        if (hold.charAt(0) == '-') {  //if negative, parse then multiply by -1
                            parsed = Integer.parseInt(hold.substring(1, hold.length())) * -1;
                        } else {
                            parsed = Integer.parseInt(hold);
                        }
                        if (stack.isEmpty()) { // check if stack is empty after getting first number
                            push(tempHold, stack);
                            push(error, stack);
                        } else {
                            if (validTop(stack)) { //check if second number is an actual number
                                hold2 = stack.pop().toString();
                                tempHold2 = hold2;
                                //      System.out.println(hash.get(hold2));

                                if ((Character.isDigit(hold2.charAt(0)) == false && hold2.charAt(0)!='-') && hash.containsKey(hold2) == false) {
                                    push(tempHold2, stack);
                                    push(tempHold, stack);
                                    push(error, stack);
                                } else {
                                    if (hash.containsKey(hold2)) { //check if it's in hashmap
                                        if (Character.isDigit(hash.get(hold2).charAt(0)) == false) {
                                            push(tempHold2, stack);
                                            push(tempHold, stack);
                                            push(error, stack);
                                            return letCounter;
                                        } else {
                                            hold2 = hash.get(hold2);
                                        }
                                    }
                                    if (hold2.charAt(0) == '-') { //if negative mult by -1
                                        parsed2 = Integer.parseInt(hold2.substring(1)) * -1;
                                    } else {
                                        parsed2 = Integer.parseInt(hold2);
                                    }
                                    if(parsed > parsed2){
                                        push(":true:", stack);
                                    } else {
                                        push(":false:", stack);
                                    }
                                }
                            } else { //if second number is not valid, error
                                push(tempHold, stack);
                                push(error, stack);
                            }
                        }
                    }
                } else { //if first number is not valid, error
                    push(error, stack);
                }

            }


        }

        /****************************************** Push ******************************************/

        if (lineRead.contains("push")) {
            hold = lineRead.substring(5, lineRead.length());
            if (hold.contains(".")) {
                stack.push(error); //throw error if decimal
            } else if (hold.contains("-") && Character.isLetter(hold.charAt(1))) {
                stack.push(error); //throw error if negative nonnumerical value
            } else if (hold.contains("-0")) {
                stack.push("0"); //-0 becomes 0
            } else {
                stack.push(hold);
            }

        }
        /****************************************** Cat ******************************************/
        if (lineRead.equals("cat")) {
            String tempHold = "";
            String tempHold2 = "";

            //  System.out.println(stack.peek().toString());
            if ((!stack.peek().toString().contains("\"") && (!hash.containsKey(stack.peek().toString())||(hash.containsKey(stack.peek().toString()) && !hash.get(stack.peek().toString()).contains("\""))))  || stack.isEmpty()) {
                stack.push(":error:");
            } else {

                hold = stack.pop().toString();
                tempHold = hold;
                // System.out.println(hold);
                if (hash.containsKey(hold)) {
                    hold = hash.get(hold);
                }


                if ((!stack.peek().toString().contains("\"") && (!hash.containsKey(stack.peek().toString())||(hash.containsKey(stack.peek().toString()) && !hash.get(stack.peek().toString()).contains("\""))))  || stack.isEmpty()) {
                    push(tempHold, stack);
                    push(error, stack);
                } else {
                    hold2 = stack.pop().toString();
                    tempHold2 = hold2;
                    if (hash.containsKey(hold2)) {
                        hold2 = hash.get(hold2);
                    }

                    push(hold2 + hold, stack);
                }
            }
        }


        /****************************************** Bind ******************************************/

        if (lineRead.equals("bind")) {
            String tempHold = "";
            String tempHold2 = "";
            if (stack.isEmpty()) {
                push(error, stack);
            } else {
                hold = stack.pop().toString();
                tempHold = hold;
                if (stack.isEmpty()) {
                    push(tempHold, stack);
                    push(error, stack);
                } else {
                    if (!hash.containsKey(hold) && (!Character.isDigit(hold.charAt(0)) && !hold.substring(0, 1).equals("\"") && !hold.substring(0, 1).equals("-") && !hold.equals(":true:") && !hold.equals(":false:") && !hold.equals(":unit:"))) {
                        push(tempHold, stack);
                        push(error, stack);
                    } else {
                        if (hash.containsKey(hold)) {
                            hold = hash.get(hold);
                        }
                        if (stack.isEmpty()) {
                            push(tempHold, stack);
                            push(error, stack);
                        } else {

                            if (Character.isDigit(stack.peek().toString().charAt(0)) || stack.peek().toString().substring(0, 1).equals("\"")) {
                                push(tempHold, stack);
                                push(error, stack);
                            } else {

                                if (hash.containsKey(hold2)) {
                                    hold2 = hash.get(hold2);
                                } else {
                                    hold2 = stack.pop().toString();
                                    hash.put(hold2, hold);
                                    stack.push(":unit:");
                                    //System.out.println(hold2);
                                }

                            }

                        }
                    }
                }



            }
        }


        /****************************************** If ******************************************/
        if (lineRead.equals("if")) {
            String tempHold = "";
            String tempHold2 = "";
            if (stack.isEmpty()) {
                push(error, stack);
            } else {
                if (validTop(stack)) {
                    hold = stack.pop().toString();
                    tempHold = hold;

                    if (hash.containsKey(hold)) {
                        hold = hash.get(hold);

                    }
                    //if true get hold, if false get hold2


                    if (stack.isEmpty()) {
                        push(tempHold, stack);
                        push(error, stack);
                    } else {
                        if (validTop(stack)) {
                            hold2 = stack.pop().toString();
                            tempHold2 = hold2;
                            if (hash.containsKey(hold2)) {
                                hold2 = hash.get(hold2);
                            }
                            if (stack.isEmpty()) {
                                push(tempHold2, stack);
                                push(tempHold, stack);
                                push(error, stack);
                            } else {
                                hold3 = stack.pop().toString();
                                if (hash.containsKey(hold3)) {
                                    hold3 = hash.get(hold3);
                                }
                                if (!hold3.equals(":true:") && !hold3.equals(":false:")) {
                                    push(tempHold2, stack);
                                    push(tempHold, stack);
                                    push(error, stack);
                                } else {
                                    if (hold3.equals(":true:")) {
                                        push(tempHold2, stack);
                                    } else {
                                        push(tempHold, stack);
                                    }
                                }
                            }
                        } else {
                            push(tempHold, stack);
                            push(error, stack);
                        }
                    }
                } else {
                    push(error, stack);
                }
            }
        }
        return letCounter;
    }


    

    public static void interpreter(String inputFile, String outputFile) {

        Stack<String> stack = new Stack<>();
        HashMap<String, String> hash = new HashMap<>();
        int letCounter = 0;

        try {

            //keep quotes in until we pring
            //to keep track of strings, keep track of their index. if index is the same as the ones being operated on, throw an error, if not, dont
            FileReader fileReader = new FileReader(inputFile);
            BufferedReader buffReader = new BufferedReader(fileReader);

            String line = "";
            while ((line = buffReader.readLine()) != null) {
                stackArray.add(line);
            }
            for (letCounter = 0; letCounter < stackArray.size(); letCounter++) {
                line = stackArray.get(letCounter);
                if (line.equals("quit")) {
                    FileWriter out = new FileWriter(outputFile, true);
                    BufferedWriter bout = new BufferedWriter(out);
                    for (int i = stack.size() - 1; i >= 0; i--) {
                        String flip = stack.peek();
                        if (flip.contains("\"")) {
                            flip = flip.replace("\"", "");
                            bout.write(flip);
                            bout.newLine();
                            stack.pop();
                           System.out.println(flip);
                        } else {

                            bout.write(flip);
                            bout.newLine();
                            stack.pop();
                            System.out.println(flip);
                        }
                    }
                    bout.close();
                    break;
                } else {
                    letCounter = checkFunction(line, stack, hash, stackArray, letCounter);
                }
            }
        } catch (IOException ex) {
            ex.printStackTrace();
        }

    }
}