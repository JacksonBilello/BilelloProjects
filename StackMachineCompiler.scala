package edu.colorado.csci3155.project1

import scala.+:

object StackMachineCompiler {

    def compileHelper(e : Expr, oList : List[StackMachineInstruction]): List[StackMachineInstruction] = {
        e match {
            case Const(c) =>
                val newList = List(PushIns(c)) ++ oList
                newList

            case Ident(i) =>
                val newList = List(StoreIns(i)) ++ oList
                newList

            case Minus(e1, e2) =>
                val newList = List(SubIns) ++ oList
                val newList1 = compileHelper(e2, newList)
                val newList2 = compileHelper(e1, newList1)
                newList2

            case Mult(e1, e2) =>
                val newList = List(MultIns) ++ oList
                val newList1 = compileHelper(e2, newList)
                val newList2 = compileHelper(e1, newList1)
                newList2

            case Plus(e1, e2) =>
                val newList = List(AddIns) ++ oList
                val newList1 = compileHelper(e2, newList)
                val newList2 = compileHelper(e1, newList1)
                newList2

            case Log(e) =>
                val newList = List(LogIns) ++ oList
                val newList1 = compileHelper(e, newList)
                newList1

            case Exp(e) =>
                val newList = List(ExpIns) ++ oList
                val newList1 = compileHelper(e, newList)
                newList1

            case Let(e1, e2, e3) =>
                val newList1 = compileHelper(e3, oList)
                val newList2 = List(LoadIns(e1)) ++ newList1
                val newList3 = compileHelper(e2, newList2)
                newList3

            case Div(e1, e2) =>
                val newList = List(DivIns) ++ oList
                val newList1 = compileHelper(e2, newList)
                val newList2 = compileHelper(e1, newList1)
                newList2

            case Sine(e) =>
                val newList = compileHelper(e, oList)
                val newList1 = List(SinIns) ++ newList
                newList1

            case Cosine(e) =>
                val newList = compileHelper(e, oList)
                val newList1 = List(CosIns) ++ newList
                newList1

        }
    }


    /* Function compileToStackMachineCode
        Given expression e as input, return a corresponding list of stack machine instructions.
        The type of stackmachine instructions are in the file StackMachineEmulator.scala in this same directory
        The type of Expr is in the file Expr.scala in this directory.
     */
    def compileToStackMachineCode(e: Expr): List[StackMachineInstruction] = {
        val outList : List[StackMachineInstruction] = List()
        val finalOutput = compileHelper(e, outList)
        finalOutput
    }
}
