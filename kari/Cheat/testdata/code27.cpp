int main(){  
    unsigned long int n,p,q;  
    while(1){  
        scanf("%d", &n);  
        if(n==0)  
            break;  
        p=0;  
        for(int i=0;i<2*n-1;i++){  
            scanf("%d",&q);  
            p=p^q;  
        }  
        printf("%d\n",p);  
    }  
    return 0;  
}