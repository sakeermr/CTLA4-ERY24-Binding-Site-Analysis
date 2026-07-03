#!/usr/bin/env python3
"""
Submit ERY2-4 docking job to HADDOCK2.4 web server
Completely automated!
"""

import requests
import json
import time
import os

HADDOCK24_URL = "https://wenmr.science.uu.nl/haddock2.4"
API_ENDPOINT = HADDOCK24_URL + "/api/rest/run"

def submit_to_haddock24(receptor_pdb, ligand_pdb, restraints_tbl, run_number=1):
    """
    Submit docking job to HADDOCK2.4 web server
    NO email verification needed!
    """
    
    print("\n" + "="*60)
    print("Submitting RUN " + str(run_number) + " to HADDOCK2.4...")
    print("="*60)
    
    # Check files exist
    if not os.path.exists(receptor_pdb):
        print("ERROR: Receptor PDB not found: " + receptor_pdb)
        return None
    
    if not os.path.exists(ligand_pdb):
        print("ERROR: Ligand PDB not found: " + ligand_pdb)
        return None
    
    if not os.path.exists(restraints_tbl):
        print("ERROR: Restraints file not found: " + restraints_tbl)
        return None
    
    # Prepare files for upload
    files = {
        'pdb_file_0': (
            'ctla4_receptor.pdb',
            open(receptor_pdb, 'rb'),
            'chemical/x-pdb'
        ),
        'pdb_file_1': (
            'ery24_ligand.pdb',
            open(ligand_pdb, 'rb'),
            'chemical/x-pdb'
        ),
        'tbl_file_0': (
            'ery24_restraints.tbl',
            open(restraints_tbl, 'rb'),
            'text/plain'
        ),
    }
    
    # Prepare data
    data = {
        'email': 'noreply@example.com',
        'docking_method': 'rigid',
        'molecule1_chain': 'C',
        'molecule2_chain': 'A',
        'ambig_inter': 'ery24_restraints.tbl',
        'run': run_number,
    }
    
    try:
        print("\nUploading to " + API_ENDPOINT + "...")
        response = requests.post(API_ENDPOINT, files=files, data=data, timeout=60)
        
        if response.status_code == 200:
            job_info = response.json()
            job_id = job_info.get('jobid')
            
            print("\n✅ SUCCESS! Job submitted!")
            print("   Job ID: " + str(job_id))
            print("   Token: " + str(job_info.get('token', 'N/A')))
            
            return {
                'run': run_number,
                'jobid': job_id,
                'token': job_info.get('token'),
                'submitted_time': time.time(),
                'status_url': HADDOCK24_URL + "/api/rest/status/" + str(job_id),
            }
        else:
            print("\n❌ Submission failed!")
            print("   Status code: " + str(response.status_code))
            print("   Response: " + response.text)
            return None
    
    except Exception as e:
        print("\n❌ Error during submission: " + str(e))
        return None

def submit_all_runs(num_runs=5):
    """Submit multiple runs"""
    
    all_jobs = []
    
    for run in range(1, num_runs + 1):
        job_info = submit_to_haddock24(
            'structures/ctla4_receptor.pdb',
            'structures/ery24_initial.pdb',
            'config/ery24_restraints.tbl',
            run_number=run
        )
        
        if job_info:
            all_jobs.append(job_info)
            print("   Run " + str(run) + "/" + str(num_runs) + " submitted!")
        else:
            print("   WARNING: Run " + str(run) + " failed to submit")
        
        # Wait between submissions
        if run < num_runs:
            print("   Waiting 20 seconds before next submission...")
            time.sleep(20)
    
    # Save all job IDs
    with open('job_ids.json', 'w') as f:
        json.dump(all_jobs, f, indent=2)
    
    print("\n" + "="*60)
    print("SUBMITTED " + str(len(all_jobs)) + " JOBS TO HADDOCK2.4")
    print("="*60)
    print("\nJob IDs saved to job_ids.json")
    
    for job in all_jobs:
        print("\nRun " + str(job['run']) + ":")
        print("  Job ID: " + str(job['jobid']))
        print("  Status: " + job['status_url'])
    
    print("\n" + "="*60)
    print("NEXT STEPS:")
    print("="*60)
    print("1. Wait 4-24 hours for jobs to complete")
    print("2. Run: python311 scripts/monitor_haddock24_job.py")
    print("3. Monitor status and auto-download results")
    print("="*60)
    
    return all_jobs

if __name__ == "__main__":
    print("\n" + "="*60)
    print("ERY2-4 TO CTLA-4 BINDING SITE DOCKING")
    print("Submitting to HADDOCK2.4 Web Server")
    print("="*60)
    
    print("\nSequence: CAWGQAILEGELAWLEGGGGGAGQLADLKRQLAWWKQAC")
    print("Target: CTLA-4 (PDB 1I8L)")
    print("Template: B7-1 binding site")
    print("Number of runs: 5 (for ensemble analysis)")
    
    # Submit jobs
    jobs = submit_all_runs(num_runs=5)
    
    if len(jobs) > 0:
        print("\n✅ Ready for monitoring!")
    else:
        print("\n❌ No jobs submitted successfully")