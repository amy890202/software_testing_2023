/*
  Ref:
  * https://llvm.org/doxygen/
  * https://llvm.org/docs/GettingStarted.html
  * https://llvm.org/docs/WritingAnLLVMPass.html
  * https://llvm.org/docs/ProgrammersManual.html
  * https://stackoverflow.com/questions/28168815/adding-a-function-call-in-my-ir-code-in-llvm
  * https://stackoverflow.com/questions/30234027/how-to-call-printf-in-llvm-through-the-module-builder-system
  * https://gite.lirmm.fr/grevy/llvm-tutorial/-/blob/master/src/exercise3bis/ReplaceFunction.cpp
 */
#include "lab-pass.h"
#include "llvm/IR/LegacyPassManager.h"
#include "llvm/IR/Module.h"
#include "llvm/IR/BasicBlock.h"
#include "llvm/IR/IRBuilder.h"
#include "llvm/IR/Constants.h"
#include "llvm/IR/GlobalVariable.h"
#include "llvm/IR/Function.h"
#include "llvm/IR/Module.h"
#include "llvm/IR/LLVMContext.h"
#include "llvm/ExecutionEngine/ExecutionEngine.h"
#include "llvm/ExecutionEngine/MCJIT.h"
#include "llvm/Support/raw_ostream.h"
#include <random>

using namespace llvm;

char LabPass::ID = 0;
//char LabPass::depth = 0;
bool LabPass::doInitialization(Module &M) {
  return true;
}

static void dumpIR(Function &F)
{
  for (auto &BB : F) {
    errs() << "BB: " << "\n";
    errs() << BB << "\n";
  }
}

static Constant* getI8StrVal(Module &M, char const *str, Twine const &name) {
  LLVMContext &ctx = M.getContext();

  Constant *strConstant = ConstantDataArray::getString(ctx, str);

  GlobalVariable *gvStr = new GlobalVariable(M, strConstant->getType(), true,
    GlobalValue::InternalLinkage, strConstant, name);

  Constant *zero = Constant::getNullValue(IntegerType::getInt32Ty(ctx));
  Constant *indices[] = { zero, zero };
  Constant *strVal = ConstantExpr::getGetElementPtr(Type::getInt8PtrTy(ctx),
    gvStr, indices, true);

  return strVal;
}

static FunctionCallee printspacePrototype(Module &M) {
  LLVMContext &ctx = M.getContext();

  FunctionType *printfType = FunctionType::get(
    Type::getInt32Ty(ctx),
    { Type::getInt8PtrTy(ctx) },
    true);

  FunctionCallee printfCallee = M.getOrInsertFunction("printf", printfType);

  return printfCallee;
}

static FunctionCallee printfPrototype(Module &M) {
  LLVMContext &ctx = M.getContext();

  FunctionType *printfType = FunctionType::get(
    Type::getInt32Ty(ctx),
    { Type::getInt8PtrTy(ctx) },
    true);

  FunctionCallee printfCallee = M.getOrInsertFunction("printf", printfType);

  return printfCallee;
}

FunctionCallee createIncrementDepthFunction(Module &M) {
  LLVMContext &Ctx = M.getContext();
  
  // Get a pointer to the global variable "depth".
  GlobalVariable *DepthVar = M.getGlobalVariable("depth");
  if (!DepthVar) {
    DepthVar = new GlobalVariable(
      M,
      Type::getInt32Ty(Ctx),
      false,
      GlobalValue::CommonLinkage,
      ConstantInt::get(Type::getInt32Ty(Ctx), 0),
      "depth"
    );
  }
  
  // Create a function that increments the "depth" variable.
  FunctionType *IncrementDepthFnType = FunctionType::get(
    Type::getVoidTy(Ctx),
    {},
    false
  );
  Function *IncrementDepthFn = Function::Create(
    IncrementDepthFnType,
    GlobalValue::InternalLinkage,
    "increment_depth",
    &M
  );
  
  // Create a basic block inside the function.
  BasicBlock *EntryBB = BasicBlock::Create(Ctx, "entry", IncrementDepthFn);
  
  // Create an IR builder for the basic block.
  IRBuilder<> Builder(EntryBB);
  
  Value *DepthValue = Builder.CreateLoad(Type::getInt32Ty(Ctx), DepthVar);
  errs() << "njknkjn" << DepthValue <<"hhuk";
  // Increment the "depth" variable.
  Value *IncrementedValue = Builder.CreateAdd(DepthValue, ConstantInt::get(Type::getInt32Ty(Ctx), 1));
  
  // Store the incremented value back into the "depth" variable.
  Builder.CreateStore(IncrementedValue, DepthVar);
  
  // Create a return instruction.
  Builder.CreateRetVoid();
  
  // Return a FunctionCallee to the newly created function.
  return IncrementDepthFn;
}

void printFunctionAddress(Function *F) {
  if (F) {
    errs() << "Function " << F->getName() << " is at address " << F << "\n";
  }
}



bool LabPass::runOnModule(Module &M) {
  errs() << "runOnModule\n";

  LLVMContext &ctx = M.getContext();

 
  GlobalVariable *DepthVar = M.getGlobalVariable("depth");
  if (!DepthVar) {
    DepthVar = new GlobalVariable(
      M,
      Type::getInt32Ty(ctx),
      false,
      GlobalValue::CommonLinkage,
      ConstantInt::get(Type::getInt32Ty(ctx), 0),
      "depth"
    );
  }

  std::random_device randDev;
  std::default_random_engine randEngine(randDev());
  std::uniform_int_distribution<unsigned int> uniformDist(0, 0xffffffff);


  FunctionCallee printfCallee = printfPrototype(M);
  //FunctionCallee IncrementDepthCallee = createIncrementDepthFunction(M);
  Constant *stackBofMsg = getI8StrVal(M, "!!!STACK BOF!!!\n", "stackBofMsg");

  for (auto &F : M) {
    if (F.empty()) {
      continue;
    }

    errs() << F.getName() << "\n";
    // Function *Fa = &F;
    // printFunctionAddress(Fa);
    // void *FuncAddr = EE->getPointerToFunction(&F);
    // errs() << F.getName() << " : " << FuncAddr << "\n";



    BasicBlock &Bstart = F.front();
    BasicBlock &Bend = F.back();

    if (Bend.empty()) // || Bend.getTerminator()->getNumSuccessors() == 0
    {
      continue;
    }
    //depth = depth+1;
    //errs()<< depth << "ddd";
    // Split "ret" from original basic block
    Instruction &ret = *(++Bend.rend());
    BasicBlock *Bret = Bend.splitBasicBlock(&ret, "ret");

    // Create epilogue BB before ret BB
    BasicBlock *Bepi = BasicBlock::Create(ctx, "epi", &F, Bret);

    // Create BB handling stack-based buffer overflow after epilogue BB (before ret BB)
    BasicBlock *Bbof = BasicBlock::Create(ctx, "bof", &F, Bret);

    // Patch the instruction at end of of Bend BB, "br ret", to "br epi"
    Instruction &br = *(++Bend.rend());
    IRBuilder<> BuilderBr(&br);
    BuilderBr.CreateBr(Bepi);
    br.eraseFromParent();

    // GlobalVariable* GV = M.getGlobalVariable("depth", true);
    // Constant* C = GV->getInitializer();
    // errs() << "The value of depth before store: " << C->getUniqueInteger() << "\n";

    // Insert code at prologue
    Instruction &Istart = Bstart.front();
    IRBuilder<> BuilderStart(&Istart);

    Value *LoadAfterStore = BuilderStart.CreateLoad(Type::getInt32Ty(ctx), DepthVar);
   
    // Create a global string containing the format string.
    // Create a named global variable for the format string.
    GlobalVariable* fmtStr = new GlobalVariable(
        M,
        llvm::ArrayType::get(Type::getInt8Ty(ctx), sizeof("%.*s")),
        true,
        GlobalValue::LinkageTypes::PrivateLinkage,
        nullptr,
        ".fmtstr");
    fmtStr->setInitializer(llvm::ConstantDataArray::getString(ctx, "%.*s"));
    fmtStr->setAlignment(llvm::MaybeAlign(1));

    // Create a constant integer value representing the precision of the string.
    //GlobalVariable* dep = M.getGlobalVariable("depth", true);
    Value* precisionVal = BuilderStart.CreateLoad(Type::getInt32Ty(ctx), DepthVar);
    //Value* precisionVal = ConstantInt::get(Type::getInt32Ty(ctx), dep);
    
    // Create a global string containing the input string.
    // Create a named global variable for the input string.
    GlobalVariable* inputStr = new GlobalVariable(
        M,
        llvm::ArrayType::get(Type::getInt8Ty(ctx), sizeof("                                                   ")),
        true,
        GlobalValue::LinkageTypes::PrivateLinkage,
        llvm::ConstantDataArray::getString(ctx, "                                                   "),
        ".inputstr");
    inputStr->setAlignment(llvm::MaybeAlign(1));

    // Get a pointer to the input string.
    //Value* inputStrPtr = BuilderStart.CreatePointerCast(inputStr, llvm::PointerType::get(llvm::ArrayType::get(Type::getInt8Ty(ctx), sizeof("############################################"))*, 0));
    Value* inputStrPtr = BuilderStart.CreatePointerCast(inputStr, Type::getInt8PtrTy(ctx));
    // Create a call to printf.
    BuilderStart.CreateCall(printfCallee, {fmtStr, precisionVal, inputStrPtr});

    LoadInst *Load = BuilderStart.CreateLoad(Type::getInt32Ty(ctx), DepthVar);
    Value *Inc = BuilderStart.CreateAdd(BuilderStart.getInt32(1), Load);
    StoreInst *Store = BuilderStart.CreateStore(Inc, DepthVar);
   

    Function *Fp = &F;
    BuilderStart.CreateCall(printfCallee, { getI8StrVal(M, (F.getName()+": %p\n").str().c_str(), "stackBofMsg"),BuilderStart.CreatePtrToInt(Fp,Type::getInt64Ty(ctx)) });
    
  

    // New basic block for handling stack-based buffer overflow
    IRBuilder<> BuilderBof(Bbof);
    LoadInst *LoadDep = BuilderBof.CreateLoad(Type::getInt32Ty(ctx), DepthVar);
    Value *Incn = BuilderBof.CreateAdd(BuilderStart.getInt32(-1), LoadDep);
    StoreInst *Storen = BuilderBof.CreateStore(Incn, DepthVar);
    BuilderBof.CreateBr(Bret);
    // Insert code at epilogue
    IRBuilder<> BuilderEnd(Bepi);
  
    BuilderEnd.CreateBr(Bbof);
    // Dump IR
    //dumpIR(F);
  }

  return true;
}

static RegisterPass<LabPass> X("labpass", "Lab Pass", false, false);