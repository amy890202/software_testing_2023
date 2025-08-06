import unittest
import Students

class Test(unittest.TestCase):
    students = Students.Students()

    user_name = ['John', 'Mary','Thomas','Jane']
    user_id = []


    # test case function to check the Students.set_name function
    def test_0_set_name(self):
        #TODO
        print("OK")
        print("Start set_name test")
        print("")
        for name in self.user_name:
            id = self.students.set_name(name)
            for id_test in self.user_id:
                self.assertNotEqual(id, id_test)
            self.user_id.append(id)
            print(id , " " , name)
        print("")
        print("Finish set_name test")
        print("")
        pass

    # test case function to check the Students.get_name function
    def test_1_get_name(self):
        #TODO
        print("")
        print("Start get_name test")
    
       
        self.assertEqual(len(self.user_id), len(self.user_name))
        print("user_id length =  ",len(self.user_id))
        print("user_name length =  ", len(self.user_name))
        print("")
       
        for i in range(len(self.user_name)):
            self.assertEqual(self.students.get_name(self.user_id[i]), self.user_name[i])
            print("id ",self.user_id[i], " : ", self.students.get_name(self.user_id[i]))
       
        mex = 0 
        while mex in self.user_id:
            mex = mex + 1
        #print(mex)
        self.assertEqual(self.students.get_name(mex), 'There is no such user')
        print("id ",mex, " : ", self.students.get_name(mex))
        print("Finish get_name test")
        pass



# if __name__ == '__main__':
#     unittest.main()
