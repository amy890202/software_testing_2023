import org.junit.Assert;
import org.junit.Test;

public class CalTest {
    // Normal year
    @Test
    public void test1() {
        Assert.assertEquals(59, Cal.cal(1, 1, 3, 1, 2022));
    }

    // // leap year
    // @Test
    // public void test2() {
    // Assert.assertEquals(121, Cal.cal(1, 1, 5, 1, 2020));
    // }

    // (m100 == 0) && (m400 != 0)
    @Test
    public void test2() {
        Assert.assertEquals(181, Cal.cal(1, 1, 7, 1, 2100));
    }

    @Test
    public void test3() {
        Assert.assertEquals(2, Cal.cal(3, 1, 3, 3, 2022));// kill AOIS_10
    }

    @Test
    public void test4() {
        Assert.assertEquals(29, Cal.cal(2, 1, 3, 1, 2012));// 17
    }

    @Test
    public void test5() {
        Assert.assertEquals(28, Cal.cal(2, 1, 3, 1, 1900));// 正常程式判斷是28天，變異程式判為29天 kill 21 22
    }

    @Test
    public void test6() {
        Assert.assertEquals(29, Cal.cal(2, 1, 3, 1, 2000));// 正常程式判斷是29天，變異程式判為28天 kill 25 26
    }

    // the below testcases dont consider preconditions

    @Test
    public void test7() {
        Assert.assertEquals(28, Cal.cal(2, 1, 1, 1, 2100));// 正常程式判斷是29天，變異程式判為28天 kill ROR4
    }

    @Test
    public void test8() {
        Assert.assertEquals(28, Cal.cal(2, 1, 3, 1, -2001));// kill ROR8
    }

    @Test
    public void test9() {
        Assert.assertEquals(29, Cal.cal(2, 1, 3, 1, -2004));// kill ROR18
    }

    @Test
    public void test10() {
        Assert.assertEquals(28, Cal.cal(2, 1, 3, 1, -500));// kill ROR22
    }

    // @Test
    // public void test9() {
    // Assert.assertEquals(29, Cal.cal(2, 1, 3, 1, 0));// 正常程式判斷是29天，變異程式判為28天 kill
    // 25 26
    // }

}

// AOIS_11 12 15 16應該是Equivalent mutants（等價突變）
// 27 28
// 31 32 35 36 39 40ssss
// 43 44 51 52 55 56
// 71 72
// 73 74
// AO 4 5 6
// COR 4 || ^
