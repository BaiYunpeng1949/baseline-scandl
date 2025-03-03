function wbNew = calcNewBoundsFunc(wb)
// The calcNewBoundsFunc.m is a MATLAB function that processes word boundaries (coordinates) for text display in the ZuCo 
// experiment. Let me break down its main functionality:
// Purpose: It adjusts the boundaries of words in a text display to create more natural reading spaces between words.
// Line Detection, Word Boundary Adjustment, Adjustment Rules, Line Transition Detection,

for i=1:length(wb)
    
    currBo= wb{i};
    currBoNew=[];
    newLine=1;
    for ii=1:size(currBo,1)
        % if in new line
        if newLine
            %if word is in 1. line
            if currBo(ii,2) >70 && currBo(ii,2) <100
                if ii<size(currBo,1) && currBo(ii+1,2)< (currBo(ii,2)+20) % if next word is in same line
                    newLine=0;
                    currBoNew(ii,1)= currBo(ii,1)-3; %left border
                    currBoNew(ii,2)= currBo(ii,2); % top vorder
                    currBoNew(ii,3)= (currBo(ii,3)+currBo(ii+1,1))/2; %right border
                    currBoNew(ii,4)= currBo(ii,4); %bottom border
                elseif ii<size(currBo,1) && currBo(ii+1,2)>= (currBo(ii,2)+20) %if next word is in new line
                    %should never happen, if in new line the next word id
                    %not in next line
                    disp(['i:' num2str(i) ', ii:' num2str(ii), 'currBo(ii,1):' num2str(currBo(ii+1,2)) ', currBo(ii+1,2):' num2str(currBo(ii+1,2))]);
                    disp('err')
                    newLine=1;
                elseif ii==size(currBo,1) %if last word of sentence:
                    currBoNew(ii,1)= currBo(ii,1)-3; %left border
                    currBoNew(ii,2)= currBo(ii,2) % top border
                    currBoNew(ii,3)= currBo(ii,3)+3; %right border
                    currBoNew(ii,4)= currBo(ii,4); %bottom border
                end
            end
            
            %if word is in 2. line
            if currBo(ii,2) >125 && currBo(ii,2) <150
                if ii<size(currBo,1) && currBo(ii+1,2)< (currBo(ii,2)+20) % if next word is in same line
                    newLine=0;
                    currBoNew(ii,1)= currBo(ii,1)-3; %left border
                    currBoNew(ii,2)= currBo(ii,2); % top border
                    currBoNew(ii,3)= (currBo(ii,3)+currBo(ii+1,1))/2; %right border
                    currBoNew(ii,4)= currBo(ii,4); %bottom border
                elseif ii<size(currBo,1) && currBo(ii+1,2)>= (currBo(ii,2)+20) %if next word is in new line
                    disp('err')
                    %should never happen, if in new line the next word id
                    %not in next line
                    newLine=1;
                elseif ii==size(currBo,1) %if last word of sentence:
                    currBoNew(ii,1)= currBo(ii,1)-3; %left border
                    currBoNew(ii,2)= currBo(ii,2); % top border
                    currBoNew(ii,3)= currBo(ii,3)+3; %right border
                    currBoNew(ii,4)= currBo(ii,4); %bottom border
                end
            end
            
            %if word is in 3. line
            if currBo(ii,2) >185 && currBo(ii,2) <205
                if ii<size(currBo,1) && currBo(ii+1,2)< (currBo(ii,2)+20) % if next word is in same line
                    newLine=0;
                    currBoNew(ii,1)= currBo(ii,1)-3; %left border
                    currBoNew(ii,2)= currBo(ii,2); % top border
                    currBoNew(ii,3)= (currBo(ii,3)+currBo(ii+1,1))/2; %right border
                    currBoNew(ii,4)= currBo(ii,4); %bottom border
                elseif ii<size(currBo,1) && currBo(ii+1,2)>= (currBo(ii,1)+20) %if next word is in new line
                    disp('err')
                    %should never happen, if in new line the next word id
                    %not in next line
                    newLine=1;
                elseif ii==size(currBo,1) %if last word of sentence:
                    currBoNew(ii,1)= currBo(ii,1)-3; %left border
                    currBoNew(ii,2)= currBo(ii,2); % top border
                    currBoNew(ii,3)= currBo(ii,3)+3; %right border
                    currBoNew(ii,4)= currBo(ii,4); %bottom border
                end
            end
            
            %if word is in 4. line
            if currBo(ii,2) >245 && currBo(ii,2) <265
                if ii<size(currBo,1) && currBo(ii+1,2)< (currBo(ii,2)+20) % if next word is in same line
                    newLine=0;
                    currBoNew(ii,1)= currBo(ii,1)-3; %left border
                    currBoNew(ii,2)= currBo(ii,2); % top border
                    currBoNew(ii,3)= (currBo(ii,3)+currBo(ii+1,1))/2; %right border
                    currBoNew(ii,4)= currBo(ii,4); %bottom border
                elseif ii<size(currBo,1) && currBo(ii+1,2)>= (currBo(ii,2)+20) %if next word is in new line
                    disp('err')
                    %should never happen, if in new line the next word id
                    %not in next line
                    newLine=1;
                elseif ii==size(currBo,1) %if last word of sentence:
                    currBoNew(ii,1)= currBo(ii,1)-3; %left border
                    currBoNew(ii,2)= currBo(ii,2); % top border
                    currBoNew(ii,3)= currBo(ii,3)+3; %right border
                    currBoNew(ii,4)= currBo(ii,4); %bottom border
                end
            end
            
            %if word is in 5. line
            if currBo(ii,2) >305 && currBo(ii,2) <325
                if ii<size(currBo,1) && currBo(ii+1,2)< (currBo(ii,2)+20) % if next word is in same line
                    newLine=0;
                    currBoNew(ii,1)= currBo(ii,1)-3; %left border
                    currBoNew(ii,2)= currBo(ii,2); % top border
                    currBoNew(ii,3)= (currBo(ii,3)+currBo(ii+1,1))/2; %right border
                    currBoNew(ii,4)= currBo(ii,4); %bottom border
                elseif ii<size(currBo,1) && currBo(ii+1,2)>= (currBo(ii,2)+20) %if next word is in new line
                    disp('err')
                    %should never happen, if in new line the next word id
                    %not in next line
                    newLine=1;
                elseif ii==size(currBo,1) %if last word of sentence:
                    currBoNew(ii,1)= currBo(ii,1)-3; %left border
                    currBoNew(ii,2)= currBo(ii,2); % top border
                    currBoNew(ii,3)= currBo(ii,3)+3; %right border
                    currBoNew(ii,4)= currBo(ii,4); %bottom border
                end
            end
            
            %if word is in 6. line
            if currBo(ii,2) >365 && currBo(ii,2) <385
                if ii<size(currBo,1) && currBo(ii+1,2)< (currBo(ii,2)+20) % if next word is in same line
                    newLine=0;
                    currBoNew(ii,1)= currBo(ii,1)-3; %left border
                    currBoNew(ii,2)= currBo(ii,2); % top border
                    currBoNew(ii,3)= (currBo(ii,3)+currBo(ii+1,1))/2; %right border
                    currBoNew(ii,4)= currBo(ii,4); %bottom border
                elseif ii<size(currBo,1) && currBo(ii+1,2)>= (currBo(ii,1)+20) %if next word is in new line
                    disp('err')
                    %should never happen, if in new line the next word id
                    %not in next line
                    newLine=1;
                elseif ii==size(currBo,1) %if last word of sentence:
                    currBoNew(ii,1)= currBo(ii,1)-3; %left border
                    currBoNew(ii,2)= currBo(ii,2); % top border
                    currBoNew(ii,3)= currBo(ii,3)+3; %right border
                    currBoNew(ii,4)= currBo(ii,4); %bottom border
                end
            end
            
            %if word is in 7. line
            if currBo(ii,2) >425 && currBo(ii,2) <445
                if ii<size(currBo,1) && currBo(ii+1,2)< (currBo(ii,2)+20) % if next word is in same line
                    newLine=0;
                    currBoNew(ii,1)= currBo(ii,1)-3; %left border
                    currBoNew(ii,2)= currBo(ii,2); % top border
                    currBoNew(ii,3)= (currBo(ii,3)+currBo(ii+1,1))/2; %right border
                    currBoNew(ii,4)= currBo(ii,4); %bottom border
                elseif ii<size(currBo,1) && currBo(ii+1,2)>= (currBo(ii,2)+20) %if next word is in new line
                    disp('err')
                    %should never happen, if in new line the next word id
                    %not in next line
                    newLine=1;
                elseif ii==size(currBo,1) %if last word of sentence:
                    currBoNew(ii,1)= currBo(ii,1)-3; %left border
                    currBoNew(ii,2)= currBo(ii,2); % top border
                    currBoNew(ii,3)= currBo(ii,3)+3; %right border
                    currBoNew(ii,4)= currBo(ii,4); %bottom border
                end
            end
            
            
            % ##### if not the first word in line: ###################################
        else
            %if word is in 1. line
            if currBo(ii,2) >70 && currBo(ii,2) <100
                if ii<size(currBo,1) && currBo(ii+1,2)< (currBo(ii,2)+20) % if next word is in same line
                    newLine=0;
                    currBoNew(ii,1)= (currBo(ii-1,3)+currBo(ii,1))/2; %left border
                    currBoNew(ii,2)= currBo(ii,2); % top vorder
                    currBoNew(ii,3)= (currBo(ii,3)+currBo(ii+1,1))/2; %right border
                    currBoNew(ii,4)= currBo(ii,4); %bottom border
                elseif ii<size(currBo,1) && currBo(ii+1,2)>= (currBo(ii,2)+20) %if next word is in new line
                    newLine=1;
                    currBoNew(ii,1)= (currBo(ii-1,3)+currBo(ii,1))/2; %left border
                    currBoNew(ii,2)= currBo(ii,2); % top vorder
                    currBoNew(ii,3)= currBo(ii,3)+3; %right border
                    currBoNew(ii,4)= currBo(ii,4); %bottom border
                elseif ii==size(currBo,1) %if last word of sentence:
                    currBoNew(ii,1)= (currBo(ii-1,3)+currBo(ii,1))/2; %left border
                    currBoNew(ii,2)= currBo(ii,2); % top border
                    currBoNew(ii,3)= currBo(ii,3)+3; %right border
                    currBoNew(ii,4)= currBo(ii,4); %bottom border
                end
            end
            
            %if word is in 2. line
            if currBo(ii,2) >125 && currBo(ii,2) <150
                if ii<size(currBo,1) && currBo(ii+1,2)< (currBo(ii,2)+20) % if next word is in same line
                    newLine=0;
                    currBoNew(ii,1)= (currBo(ii-1,3)+currBo(ii,1))/2; %left border
                    currBoNew(ii,2)= currBo(ii,2); % top border
                    currBoNew(ii,3)= (currBo(ii,3)+currBo(ii+1,1))/2; %right border
                    currBoNew(ii,4)= currBo(ii,4); %bottom border
                elseif ii<size(currBo,1) && currBo(ii+1,2)>= (currBo(ii,2)+20) %if next word is in new line
                    newLine=1;
                    currBoNew(ii,1)= (currBo(ii-1,3)+currBo(ii,1))/2; %left border
                    currBoNew(ii,2)= currBo(ii,2); % top border
                    currBoNew(ii,3)= currBo(ii,3)+3; %right border
                    currBoNew(ii,4)= currBo(ii,4); %bottom border
                elseif ii==size(currBo,1) %if last word of sentence:
                    currBoNew(ii,1)= (currBo(ii-1,3)+currBo(ii,1))/2; %left border
                    currBoNew(ii,2)= currBo(ii,2); % top border
                    currBoNew(ii,3)= currBo(ii,3)+3; %right border
                    currBoNew(ii,4)= currBo(ii,4); %bottom border
                end
            end
            
            %if word is in 3. line
            if currBo(ii,2) >185 && currBo(ii,2) <205
                if ii<size(currBo,1) && currBo(ii+1,2)< (currBo(ii,2)+20) % if next word is in same line
                    newLine=0;
                    currBoNew(ii,1)= (currBo(ii-1,3)+currBo(ii,1))/2; %left border
                    currBoNew(ii,2)= currBo(ii,2); % top border
                    currBoNew(ii,3)= (currBo(ii,3)+currBo(ii+1,1))/2; %right border
                    currBoNew(ii,4)= currBo(ii,4); %bottom border
                elseif ii<size(currBo,1) && currBo(ii+1,2)>= (currBo(ii,2)+20) %if next word is in new line
                    newLine=1;
                    currBoNew(ii,1)= (currBo(ii-1,3)+currBo(ii,1))/2; %left border
                    currBoNew(ii,2)= currBo(ii,2); % top border
                    currBoNew(ii,3)= currBo(ii,3)+3; %right border
                    currBoNew(ii,4)= currBo(ii,4); %bottom border
                elseif ii==size(currBo,1) %if last word of sentence:
                    currBoNew(ii,1)= (currBo(ii-1,3)+currBo(ii,1))/2; %left border
                    currBoNew(ii,2)= currBo(ii,2); % top border
                    currBoNew(ii,3)= currBo(ii,3)+3; %right border
                    currBoNew(ii,4)= currBo(ii,4); %bottom border
                end
            end
            
            %if word is in 4. line
            if currBo(ii,2) >245 && currBo(ii,2) <265
                if ii<size(currBo,1) && currBo(ii+1,2)< (currBo(ii,2)+20) % if next word is in same line
                    newLine=0;
                    currBoNew(ii,1)= (currBo(ii-1,3)+currBo(ii,1))/2; %left border
                    currBoNew(ii,2)= currBo(ii,2); % top border
                    currBoNew(ii,3)= (currBo(ii,3)+currBo(ii+1,1))/2; %right border
                    currBoNew(ii,4)= currBo(ii,4); %bottom border
                elseif ii<size(currBo,1) && currBo(ii+1,2)>= (currBo(ii,2)+20) %if next word is in new line
                    newLine=1;
                    currBoNew(ii,1)= (currBo(ii-1,3)+currBo(ii,1))/2;; %left border
                    currBoNew(ii,2)= currBo(ii,2); % top border
                    currBoNew(ii,3)= currBo(ii,3)+3; %right border
                    currBoNew(ii,4)= currBo(ii,4); %bottom border
                elseif ii==size(currBo,1) %if last word of sentence:
                    currBoNew(ii,1)= (currBo(ii-1,3)+currBo(ii,1))/2; %left border
                    currBoNew(ii,2)= currBo(ii,2); % top border
                    currBoNew(ii,3)= currBo(ii,3)+3; %right border
                    currBoNew(ii,4)= currBo(ii,4); %bottom border
                end
            end
            
            %if word is in 5. line
            if currBo(ii,2) >305 && currBo(ii,2) <325
                if ii<size(currBo,1) && currBo(ii+1,2)< (currBo(ii,2)+20) % if next word is in same line
                    newLine=0;
                    currBoNew(ii,1)= (currBo(ii-1,3)+currBo(ii,1))/2; %left border
                    currBoNew(ii,2)= currBo(ii,2); % top border
                    currBoNew(ii,3)= (currBo(ii,3)+currBo(ii+1,1))/2; %right border
                    currBoNew(ii,4)= currBo(ii,4); %bottom border
                elseif ii<size(currBo,1) && currBo(ii+1,2)>= (currBo(ii,2)+20) %if next word is in new line
                    newLine=1;
                    currBoNew(ii,1)= (currBo(ii-1,3)+currBo(ii,1))/2; %left border
                    currBoNew(ii,2)= currBo(ii,2); % top border
                    currBoNew(ii,3)= currBo(ii,3)+3; %right border
                    currBoNew(ii,4)= currBo(ii,4); %bottom border
                elseif ii==size(currBo,1) %if last word of sentence:
                    currBoNew(ii,1)= (currBo(ii-1,3)+currBo(ii,1))/2; %left border
                    currBoNew(ii,2)= currBo(ii,2); % top border
                    currBoNew(ii,3)= currBo(ii,3)+3; %right border
                    currBoNew(ii,4)= currBo(ii,4); %bottom border
                end
            end
            
            %if word is in 6. line
            if currBo(ii,2) >365 && currBo(ii,2) <385
                if ii<size(currBo,1) && currBo(ii+1,2)< (currBo(ii,2)+20) % if next word is in same line
                    newLine=0;
                    currBoNew(ii,1)= (currBo(ii-1,3)+currBo(ii,1))/2; %left border
                    currBoNew(ii,2)= currBo(ii,2); % top border
                    currBoNew(ii,3)= (currBo(ii,3)+currBo(ii+1,1))/2; %right border
                    currBoNew(ii,4)= currBo(ii,4); %bottom border
                elseif ii<size(currBo,1) && currBo(ii+1,2)>= (currBo(ii,2)+20) %if next word is in new line
                    newLine=1;
                    currBoNew(ii,1)= (currBo(ii-1,3)+currBo(ii,1))/2; %left border
                    currBoNew(ii,2)= currBo(ii,2); % top border
                    currBoNew(ii,3)= currBo(ii,3)+3; %right border
                    currBoNew(ii,4)=currBo(ii,4); %bottom border
                elseif ii==size(currBo,1) %if last word of sentence:
                    currBoNew(ii,1)= (currBo(ii-1,3)+currBo(ii,1))/2; %left border
                    currBoNew(ii,2)= currBo(ii,2); % top border
                    currBoNew(ii,3)= currBo(ii,3)+3; %right border
                    currBoNew(ii,4)= currBo(ii,4); %bottom border
                end
            end
            
            %if word is in 7. line
            if currBo(ii,2) >425 && currBo(ii,2) <445
                if ii<size(currBo,1) && currBo(ii+1,2)< (currBo(ii,2)+20) % if next word is in same line
                    newLine=0;
                    currBoNew(ii,1)= (currBo(ii-1,3)+currBo(ii,1))/2; %left border
                    currBoNew(ii,2)= currBo(ii,2); % top border
                    currBoNew(ii,3)= (currBo(ii,3)+currBo(ii+1,1))/2; %right border
                    currBoNew(ii,4)= currBo(ii,4); %bottom border
                elseif ii<size(currBo,1) && currBo(ii+1,2)>= (currBo(ii,2)+20) %if next word is in new line
                    newLine=1;
                    currBoNew(ii,1)= (currBo(ii-1,3)+currBo(ii,1))/2; %left border
                    currBoNew(ii,2)= currBo(ii,2); % top border
                    currBoNew(ii,3)= currBo(ii,3)+3; %right border
                    currBoNew(ii,4)= currBo(ii,4); %bottom border
                elseif ii==size(currBo,1) %if last word of sentence:
                    currBoNew(ii,1)= (currBo(ii-1,3)+currBo(ii,1))/2; %left border
                    currBoNew(ii,2)= currBo(ii,2); % top border
                    currBoNew(ii,3)= currBo(ii,3)+3; %right border
                    currBoNew(ii,4)= currBo(ii,4); %bottom border
                end
            end
            
            
        end
        
    end
%     clf;
%     
%     axis([0 800 0 600])
%     hold on
%     for ij=1:size(currBoNew,1)
%         rectangle('Position',[currBoNew(ij,1) (currBoNew(ij,2)) (currBoNew(ij,3)-currBoNew(ij,1)) (currBoNew(ij,4)-currBoNew(ij,2))]);
%     end
%     hold off;
%     set (gca,'YDir','reverse')
%     
%     k=waitforbuttonpress;
    
    
    
    wbNew{i}=currBoNew;
    
end


end