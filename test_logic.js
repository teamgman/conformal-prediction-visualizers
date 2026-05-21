const n_2 = 20;
for(let trial=0; trial<1000; trial++) {
    let residuals = [];
    for(let i=0; i<20; i++) residuals.push(Math.random() * 10);
    residuals.sort((a,b) => a-b);
    for(let k=1; k<=21; k++) {
        let R_k = (k <= n_2) ? residuals[k-1] : Infinity;
        for(let v_score = -1; v_score < 12; v_score += 0.1) {
            let crimsonCount = 0;
            for(let i=0; i<n_2; i++) {
                if (residuals[i] < v_score) crimsonCount++;
            }
            let eq1 = k > n_2 ? true : (v_score <= R_k);
            let eq2 = eq1;
            let eq3 = (crimsonCount / n_2) < (k / n_2);
            if (!(eq1 === eq2 && eq2 === eq3)) {
                console.log(`Broke! k=${k}, V=${v_score.toFixed(3)}, R_k=${R_k.toFixed(3)}, crimson=${crimsonCount}, eq1=${eq1}, eq3=${eq3}`);
                process.exit(1);
            }
        }
    }
}
console.log("All good");
