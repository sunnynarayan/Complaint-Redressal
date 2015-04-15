import java.util.*;
public class pancake 
{
    public static void main(String args[]) 
    {
        Scanner in=new Scanner(System.in);
        int test;
        test=in.nextInt();
        for (int i = 0; i < test; i++) 
        {
            int n;
            n=in.nextInt();
            int arr[]=new int[n];
            for (int j = 0; j < n; j++) 
            {
                arr[j]=in.nextInt();
                
            }
            Arrays.sort(arr);
            int temp[]=new int[n];
            for (int j = 0; j < n; j++)
            {
                temp[j]=arr[n-j-1];
            }
            int min=0;
            int te=0;
            int j=0;
                while(j<n&&temp[j]>0)
                {
                    int k=0;
                    while(temp[j]>3)
                    {
                       temp[j]=temp[j]/2;
                       min=min+(int)Math.pow(2,k);
                       ++k;
                    }
                    for (int l =j+1; l < n; l++) 
                    {
                        temp[l]=temp[l]-temp[j];
                        
                    }
                    min=min+temp[j];
                    te=min;
                ++j;
                
                 
            }
                System.out.println("Case #"+(i+1)+": "+min);
            
        }
    }
}
