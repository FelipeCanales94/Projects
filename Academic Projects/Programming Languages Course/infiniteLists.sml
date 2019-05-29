datatype 'a inflist = NIL
                    | CONS of 'a * (unit -> 'a inflist);

exception Empty;
exception Subscript;

fun HD (CONS(a,b)) = a
  | HD NIL = raise Empty; 

fun TL (CONS(a,b)) = b()
  | TL NIL = raise Empty;

fun NUL NIL = true
  | NUL _ = false;

fun NTH 0 L = HD L
  | NTH n L = NTH (n-1) (TL L);

fun TAKE (xs, 0) = []
  | TAKE (NIL, n) = raise Subscript
  | TAKE (CONS(x, xf), n) = x::TAKE(xf(), n-1);

fun FROMN n = CONS(n, fn () => FROMN (n+1));
fun GETALLZERO n = CONS(n, fn() => GETALLZERO (0));
fun GETALLONE n = CONS(n, fn() => GETALLONE(1));


fun FIB n m = CONS(n, fn () => FIB m (n+m));

fun FILTER f l =
  if NUL l
  then NIL
  else if f (HD l)
       then CONS(HD l, fn() => (FILTER f (TL l)))
       else FILTER f (TL l);

fun SIFT NIL = NIL
  | SIFT l =
     let val a = HD l
     in CONS(a, fn () => SIFT(FILTER (fn x => x mod a <> 0) (TL l)))
     end;

	 
fun even (x : int) : bool = if x mod 2 = 0 then true else false;
fun odd  (x : int) : bool = if x mod 2 = 1 then true else false;
(**********************
 *
 * FUNCTION AND INFLIST STUBS -- YOU MUST IMPLEMENT THESE
 * 
 * printList and printPairList must write to the file named by f.
 * Anything printed to the terminal will not be graded.
 *
 **********************)
 
val infiniteList = FROMN 0;
val infiniteList2 = FROMN 2;


val fibs  = FIB 0 1;
(*Check if number is even or odd*)
val evens = FILTER even infiniteList;
val odds  = FILTER odd infiniteList;


(*Creates infinite list of all 0s or all 1s*)
val allZeros =  GETALLZERO 0;
val allOnes  = GETALLONE 1;

(*Prime List*)
val primes = SIFT infiniteList2;

(*PrintGen Function*)
fun printGenList (f : ('a -> 'b)) (l : ('a list)) : unit = 
  case l of 
    [] => () 
  | y::ys => (f(y); printGenList f ys)

fun printList (f : string, l : int list) : unit = 
  let
    (*file to write to*)
    val outputFile = TextIO.openOut f
    (*function that iterates thru an int list*)
    fun iterate(intList : int list) =  
          case intList of
              [] => (TextIO.closeOut outputFile)
              (*pattern matching. Convert int to string and add space*)
            | y::ys => (TextIO.output(outputFile, Int.toString(y) ^ " "); iterate(ys))
  in
    iterate(l)
  end
  
fun printPairList (f : string, l : (int * int) list) : unit = 
   let
    (*file to write to*)
    val outputFile = TextIO.openOut f
    (*function that iterates thru an int list*)
    fun iterate(intList : (int * int) list) =  
          case intList of
              [] => (TextIO.closeOut outputFile)
              (*pattern matching. Convert int to string and add space*)
            | (y, y1)::ys => (TextIO.output(outputFile, "("^Int.toString(y) ^ ", " ^ Int.toString(y1) ^ ") "); iterate(ys))
  in
    iterate(l)
  end


fun rev_zip (infL1 : 'a inflist, infL2 : 'b inflist) : ('b * 'a) inflist = 
   case (infL1,infL2) of
    (*if infl1 or infl2 are empty, send Nil*)
        (NIL,infL2) => NIL
      | (infL1, NIL) => NIL
      (*pattern matching (a list, b list) to (head of b list, head of a list) then use recursion on tail of both lists*)
      | (CONS(x,xs), CONS(y,ys)) =>  (CONS((y,x), fn ()=> rev_zip(xs(),ys())))