from datetime import timedelta
from temporalio import workflow
from transfer_request import TransferRequest

with workflow.unsafe.imports_passed_through():
    from banking_activities import withdraw, deposit, refund


@workflow.defn
class MoneyTransferWorkflow:
    def __init__(self) -> None:
        self.approved = False
        self.approval_received = False
        # TODO: Add state tracking variables
        # - transfer_state: Track overall state (PENDING, IN_PROGRESS, COMPLETED, REJECTED)
        # - current_step: Track current processing step

    @workflow.run
    async def transfer(self, request: TransferRequest) -> str:
        workflow.logger.info(f"Starting transfer: {request}")
        
        # TODO: Update transfer_state to "IN_PROGRESS"
        # TODO: Update current_step to "WITHDRAWING"
        
        # Step 1: Execute withdraw activity with 5 second timeout
        await workflow.execute_activity(
            withdraw,
            args=[request.from_account, request.amount],
            start_to_close_timeout=timedelta(seconds=5),
        )
        
        workflow.logger.info("Withdrawal completed")
        # TODO: Update current_step to "WAITING_FOR_APPROVAL"
        
        # Step 2: Wait for approval signal using workflow.wait_condition
        workflow.logger.info("Waiting for approval...")
        await workflow.wait_condition(lambda: self.approval_received)
        
        if self.approved:
            # Step 3a: If approved, execute deposit activity
            # TODO: Update current_step to "DEPOSITING"
            await workflow.execute_activity(
                deposit,
                args=[request.to_account, request.amount],
                start_to_close_timeout=timedelta(seconds=5),
            )
            
            workflow.logger.info("Transfer approved and completed")
            # TODO: Update transfer_state to "COMPLETED"
            # TODO: Update current_step to "COMPLETED"
            return "Transfer completed successfully"
        else:
            # Step 3b: If not approved, execute refund activity
            # TODO: Update current_step to "REFUNDING"
            await workflow.execute_activity(
                refund,
                args=[request.from_account, request.amount],
                start_to_close_timeout=timedelta(seconds=5),
            )
            
            workflow.logger.info("Transfer rejected and refunded")
            # TODO: Update transfer_state to "REJECTED"
            # TODO: Update current_step to "REFUNDED"
            return "Transfer rejected and refunded"

    @workflow.signal
    async def approve(self, approved: bool) -> None:
        workflow.logger.info(f"Approval received: {approved}")
        self.approved = approved
        self.approval_received = True

    @workflow.query
    def get_transfer_state(self) -> str:
        # TODO: Return the current transfer state
        pass

    @workflow.query
    def get_current_step(self) -> str:
        # TODO: Return the current processing step
        pass

    @workflow.query
    def is_approved(self) -> bool:
        # TODO: Return approval status (None if not received yet)
        pass