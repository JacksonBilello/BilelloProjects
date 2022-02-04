package edu.colorado.csci3155.project1


sealed trait StackMachineInstruction
case class LoadIns(s: String) extends StackMachineInstruction
case class  StoreIns(s: String) extends StackMachineInstruction
case class PushIns(f: Double) extends StackMachineInstruction
case object AddIns extends StackMachineInstruction
case object SubIns extends StackMachineInstruction
case object MultIns extends StackMachineInstruction
case object DivIns extends StackMachineInstruction
case object ExpIns extends StackMachineInstruction
case object LogIns extends StackMachineInstruction
case object SinIns extends StackMachineInstruction
case object CosIns extends StackMachineInstruction
case object PopIns extends StackMachineInstruction

object StackMachineEmulator {

    def popStack(stack: List[Double]): (List[Double], Double) = {
        if (stack == Nil) {
            throw new IllegalArgumentException("Empty Stack1")
        }
        val top = stack.head
        val stack1 = stack.slice(1, stack.length)
        (stack1, top)
    }

    /* Function emulateSingleInstruction
        Given a list of doubles to represent a stack
              a map from string to double precision numbers for the environment
        and   a single instruction of type StackMachineInstruction
        Return a tuple that contains the
              modified stack that results when the instruction is executed.
              modified environment that results when the instruction is executed.

        Make sure you handle the error cases: eg., stack size must be appropriate for the instruction
        being executed. Division by zero, log of a non negative number
        Throw an exception or assertion violation when error happens.
     */
    def emulateSingleInstruction(stack: List[Double],
                                 env: Environment.t,
                                 ins: StackMachineInstruction): (List[Double], Environment.t) = {
        ins match { //match instruction
            case LoadIns(i) => //if we want to load top of stack to environment
                if (stack == Nil) { //If the stack is empty
                    throw new IllegalArgumentException("Empty Stack2") //we are unable to pop from the stack.
                }
                else { //we want to pop the top value from the stack and add it to the environment
                    val (newStack, topValue) = popStack(stack)
                    val newenv = Environment.extend(i, topValue, env)
                    (newStack, newenv)
                }

            case AddIns =>
                val (st1, add1) = popStack(stack)
                val (st2, add2) = popStack(st1)
                val addStack = add1 + add2
                val newStack = addStack :: st2
                (newStack, env)

            case PushIns(d) =>
                val newStack = d :: stack
                (newStack, env)

            case ExpIns =>
                val (st1, exp1) = popStack(stack)
                val finExp = math.exp(exp1)
                val newStack = finExp :: st1
                (newStack, env)

            case LogIns =>
                val (st1, log1) = popStack(stack)
                if (log1 <= 0) {
                    throw new IllegalArgumentException("cannot take log of negative number")
                }
                else {
                    val newLog = math.log(log1)
                    val newStack = newLog :: st1
                    (newStack, env)
                }

            case StoreIns(i) =>
                val stVal = Environment.lookup(i, env)
                val newStack = stVal :: stack
                (newStack, env)

            case PopIns =>
                val (newStack, top1) = popStack(stack)
                (newStack, env)

            case SubIns =>
                val (st1, v1) = popStack(stack)
                val (st2, v2) = popStack(st1)
                val newval = v2 - v1
                val newStack = newval :: st2
                (newStack, env)

            case MultIns =>
                val (st1, mult1) = popStack(stack)
                val (st2, mult2) = popStack(st1)
                val multStack = mult1 * mult2
                val newStack = multStack :: st2
                (newStack, env)

            case DivIns =>
                val (st1, v1) = popStack(stack)
                val (st2, v2) = popStack(st1)
                val newval = v2 / v1
                val newStack = newval :: st2
                (newStack, env)

            case SinIns =>
                val (st1, v1) = popStack(stack)
                val newval = math.sin(v1)
                val newStack = newval :: st1
                (newStack, env)

            case CosIns =>
                val (st1, v1) = popStack(stack)
                val newval = math.cos(v1)
                val newStack = newval :: st1
                (newStack, env)
        }
    }

    /* Function emulateStackMachine
       Execute the list of instructions provided as inputs using the
       emulateSingleInstruction function.
       Use foldLeft over list of instruction rather than a for loop if you can.
       Return value must be a double that is the top of the stack after all instructions
       are executed.
     */
    def emulateStackMachine(instructionList: List[StackMachineInstruction]): Environment.t = {
        //val stack1 : List[Double] = List() //initialize empty stack
        //val Environ : Environment.t = Environment.empty //initialize empty environment
        val fin = instructionList.foldLeft[(List[Double], Environment.t)]((List(), Environment.empty)) {

            case ((stack, env), x) => emulateSingleInstruction(stack, env, x)
        }
        val (st, en) = fin
        en
    }
}