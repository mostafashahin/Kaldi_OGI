# Kaldi_OGI
Kaldi recipe for OGI kids data model building

**Steps**:
1. Download the OGI kids dataset inside egs directory
2. in run.sh modify OGIROOT to point to the main directory of the dataset
3. ./run.sh **This will build the HMM-GMM model
4. After completed successfully run local/nnet3/run_tdnn_delta.sh **for the TDNN model
