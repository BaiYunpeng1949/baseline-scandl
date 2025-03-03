% a) concat ET data of the current task
% b) get rid of large outliers which fixate nowhere near text
% c) correct y axis using gaussian mixture model approach

// The prepareETData.m script is a preprocessing script for eye-tracking (ET) data in the ZuCo dataset. 
// It performs the following main steps:
// 1. Concatenates ET data across multiple files for a given task and timepoint
// 2. Removes large outliers where fixations are not near text
// 3. Corrects the y-axis values using a Gaussian Mixture Model (GMM) approach


clc;
clear all;

%% params and paths:
raw='C:\Users\Marius\Downloads\NLP'

subjects={'ZAB','ZDM','ZDN','ZGW','ZJM','ZJN','ZKB','ZKH','ZKW','ZMG','ZPH'};
tasks ={'NR','SR','TSR'}


for task=tasks
    task=cell2mat(task);
    
    if strcmp(task,'SR')
        timepoints={'T1', 'T2'};
    else
        timepoints={'T1'};
    end
    
    for tp=timepoints;
        tp=cell2mat(tp);
        
        for sj=subjects
            sj=cell2mat(sj);
            
            fold=[raw filesep task filesep sj];
            
            
            %% read in worbounds:
            %change according to the task:
            if strcmp(task,'SR') && strcmp(tp,'T1')
                tmp=load([fold filesep 'wordbounds_SNR1_' sj '.mat']);
            elseif strcmp(task,'SR') && strcmp(tp,'T2')
                tmp=load([fold filesep 'wordbounds_SNR2_' sj '.mat']);
            else
                tmp=load([fold filesep 'wordbounds_' task '_' sj '.mat']);
                %tmp=load([fold filesep 'wordbounds2_' sj '_' task '.mat']);
            end
            %tmp=load([fold filesep 'wordbounds2_' sj '_NR.mat']);
            wbold= tmp.wordbounds;
            clear tmp;
            
            %% read in and load ET data
            d=dir(fold);
            cntET=1;
            if strcmp(task,'SR') && strcmp(tp,'T2')
                offset=5;
            else
                offset=0;
            end
            for i=1:length(d)
                
                if endsWith(d(i).name,['_' task  num2str(cntET+offset) '_ET.mat'])
                    % load et.mat file
                    evalc(['et' num2str(cntET) '= [ fold filesep d(i).name]']);
                    cntET=cntET+1;
                end
                
            end
            for i=1:(cntET-1)
                evalc(['etdat' num2str(i) '=load(et' num2str(i) ')']);
            end
            
            fixationData=[];
            fullData=[];
            trigger=[];
            for i=1:(cntET-1)
                evalc(['curr_etdat = etdat' num2str(i)]);
                startETDataset(i)=curr_etdat.eyeevent.fixations.data(1,1);
                endETDataset(i)=curr_etdat.eyeevent.fixations.data(end,2);
                
                fixationData = vertcat(fixationData, curr_etdat.eyeevent.fixations.data);
                fullData = vertcat(fullData,curr_etdat.data);
                trigger= vertcat (trigger, curr_etdat.event);
            end
            
            
            %% split wordbounds after linebreaks to get {worbounds per line} cell array:
            for i=1:length(wbold)
                %disp(num2str(i));
                currWBnew={};
                currWB=wbold{i};
                cntLines=1;
                %keyboard;
                %currWBnew{1}=[];
                for ii=1:size(currWB,1)-1
                    if ii==1
                        start=1;
                    end
                    %if new line begins:
                    if currWB(ii,2)+30<currWB(ii+1,2)
                        currWBnew{cntLines}=currWB(start:ii,:);
                        start=ii+1;
                        cntLines=cntLines+1;
                    end
                    %if end reached:
                    if ii==size(currWB,1)-1
                        currWBnew{cntLines}=currWB(start:ii+1,:);
                    end
                end
                if size(currWB,1)==1
                    wbLines{i}={currWB};
                else
                    % keyboard;
                    wbLines{i}=currWBnew;
                end
            end
            
            
            
            %% fit gausian mixture model to determine which fixation corresponds to which line
            
            sentenceStart= find(trigger(:,2)==10 | trigger(:,2)==12);
            sentenceStop= find(trigger(:,2)==11 | trigger(:,2)==13);
            fixationData_corrected=[];
            
            if length(wbold)== length(sentenceStart)
                stop=length(wbold);
            elseif length(wbold)> length(sentenceStart)
                disp('MORE WORDBOUNDS THAN SENTENCES!?');
                stop=length(sentenceStart);
            elseif length(wbold)< length(sentenceStart)
                disp('MORE SENTENCES THAN WORDBOUNDS!?');
                stop=length(wbold);
            end
            
            % figure;
            for i=1:stop%length(wbold)
                bo=wbLines{i};
                bo_2=wbold{i};
                startTime= trigger(sentenceStart(i),1);
                stopTime= trigger(sentenceStop(i),1);
                
                sentFixations= find(fixationData(:,1)>=startTime & fixationData(:,1)<=stopTime );
                sentData= find(fullData(:,1)>=startTime & fullData(:,1)<=stopTime );
                % saveSentFixations{i}=sentFixations;
                
                %loop through all fixations within the current sentence and remove unrealsitic data:
                allowedOffset=50;
                currfixationDataClean=[];
                %extract all fixations within the current sentence
                for ii=1:size(sentFixations,1)
                    if fixationData(sentFixations(ii),5)<bo{end}(1,4)+allowedOffset
                        currfixationDataClean(end+1,:)=fixationData(sentFixations(ii),:);
                    else
                        % disp('too far away');
                    end
                end
                
                %extract all eyedata of current sentence
                currFullEyeDataClean=[];
                for ii=1:size(sentData,1)
                    if not(fullData(sentData(ii),3)==0)
                        if fullData(sentData(ii),3)<bo{end}(1,4)+allowedOffset
                            %disp('here');
                            currFullEyeDataClean(end+1,:)=fullData(sentData(ii),:);
                        end
                    end
                end
                
                % find startvalues for gm approach :
                startVals=[];
                vari=[];
                for ii=1:size(bo,2)
                    startVals(ii)=mean([bo{1,ii}(1,2) bo{1,ii}(1,4)]);
                    vari(1,1,ii)=bo{1,ii}(1,4)-bo{1,ii}(1,2);
                end
                
                if not(isempty(currfixationDataClean)) && not(size(bo{1},1)==1)
                    S.mu=startVals';
                    X=currFullEyeDataClean(:,3);
                    S.Sigma=vari;
                    %gaussian mixture model on full data with correct startvalues:
                    M=fitgmdist(X,size(bo,2), 'CovarianceType','diagonal', 'Start',S ,'RegularizationValue',0.1 );
                    new=cluster(M,currfixationDataClean(:,5));
                    
                    %     new4_posterior=posterior(M4,currfixationDataClean(:,5));
                    %     figure;
                    %     imagesc(new4_posterior);
                    
                    
                    %match found clusters to real lines:
                    %clusterline(1)=3 means cluster 1 is acutally representing the 3rd line
                    tmp=M.mu;
                    currmin=0;
                    for ii=1:size(bo,2)
                        [xx,where]=min(tmp);
                        %clusterLine(ii) = where;
                        clusterLine(where)=ii;
                        tmp(where)=inf;
                    end
                    
                    %insert new y values in the current fixationdata
                    lineMeans=startVals;
                    currfixationDataCorrected=currfixationDataClean;
                    for ii=1:size(currfixationDataClean)
                        
                        newYVal=lineMeans(clusterLine(new(ii)));
                        %-> get the cluster of the current y val -> get the matching "real"
                        %line -> get the mean y value of this real current line
                        
                        currfixationDataCorrected(ii,5)=newYVal;
                    end
                    
                    fixationData_corrected=vertcat(fixationData_corrected, currfixationDataCorrected);
                end
                if size(bo{1},1)==1
                    disp('WORDBOUND CORRUPTED')
                elseif isempty(currfixationDataClean)
                    disp('NO FIXATIONS HERE')
                else
                    % plot #################################################################
                    %         if i>113
                    %             col=[new*20];
                    %             clf;
                    %             subplot(3,1,1);
                    %             hold on
                    %             for ij=1:size(bo_2,1)
                    %                 rectangle('Position',[bo_2(ij,1) (bo_2(ij,2)) (bo_2(ij,3)-bo_2(ij,1)) (bo_2(ij,4)-(bo_2(ij,2)))]);
                    %             end
                    %             scatter(fixationData(sentFixations,4),fixationData(sentFixations,5));
                    %             hold off
                    %
                    %             subplot(3,1,2);
                    %             scatter(currfixationDataClean(:,4),currfixationDataClean(:,5),[],col);
                    %             title('gaussian mixture model on full eyedata, with startvalues');
                    %
                    %             subplot(3,1,3);
                    %             scatter(currfixationDataCorrected(:,4),currfixationDataCorrected(:,5),[],col);
                    %             title('corrected ET data');
                    %
                    %             suptitle(['Sentence nr. ' num2str(i)]);
                    %
                    %             k = waitforbuttonpress;
                    %        end
                    %plot end #############################################################
                    
                end
                
            end
            
            %extarct corrected fixations per recordingfile:
            ii=1;
            for i=1:size(endETDataset,2)
                tmpData=[];
                while  ii<=size(fixationData_corrected,1) && fixationData_corrected(ii,1)>=startETDataset(i) &&  fixationData_corrected(ii,2) <= endETDataset(i)
                    tmpData(end+1,:)=fixationData_corrected(ii,:);
                    ii=ii+1;
                end
                fixationData_corrected_cell{i}=tmpData;
            end
            
            %overwrite fixations in original et.mat file with cleaned and corrected
            %fixations:
            for i=1:(cntET-1)
                evalc(['etdat' num2str(i) '.eyeevent.fixations.data=fixationData_corrected_cell{' num2str(i) '}']);
                evalc(['etdat' num2str(i) '.eyeevent.fixations.eye(length(fixationData_corrected_cell{' num2str(i) '})+1:end)=[]']);
            end
            
            %save the corrected ET files
            for i=1:(cntET-1)
                evalc(['save([fold filesep sj ''_'' task num2str(i+offset)  ''_corrected_ET.mat''],''-struct'', ''etdat' num2str(i) ''')']);
            end
            
        end
    end
end